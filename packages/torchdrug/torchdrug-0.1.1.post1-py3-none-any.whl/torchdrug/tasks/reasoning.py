import torch
from torch import nn
from torch.nn import functional as F
from torch.utils import data as torch_data

from torchdrug import core, tasks
from torchdrug.core import Registry as R


@R.register("tasks.KnowledgeGraphCompletion")
class KnowledgeGraphCompletion(tasks.Task, core.Configurable):
    """
    Knowledge graph completion task.

    This class provides routines for the family of knowledge graph embedding models.

    Parameters:
        model (nn.Module): knowledge graph embedding model
        criterion (str, list or dict, optional): training criterion(s). For dict, the keys are criterions and the values
            are the corresponding weights. Available criterions are ``bce``, ``ce`` and ``ranking``.
        metric (str or list of str, optional): metric(s). Available metrics are ``mr``, ``mrr`` and ``hits@K``.
        num_negative (int, optional): number of negative samples per positive sample
        margin (float, optional): margin in ranking criterion
        adversarial_temperature (float, optional): temperature for self-adversarial negative sampling.
            Set ``0`` to disable self-adversarial negative sampling.
        strict_negative (bool, optional): use strict negative sampling or not
        filtered_ranking (bool, optional): use filtered or unfiltered ranking for evaluation
        fact_ratio (float, optional): split the training set into facts and labels.
            Set ``None`` to use the whole training set as both facts and labels.
        sample_weight (bool, optional): whether to down-weight triplets from entities of large degrees
    """
    _option_members = ["criterion", "metric"]

    def __init__(self, model, criterion="bce", metric=("mr", "mrr", "hits@1", "hits@3", "hits@10"),
                 num_negative=128, margin=6, adversarial_temperature=0, strict_negative=True, filtered_ranking=True,
                 fact_ratio=None, sample_weight=True):
        super(KnowledgeGraphCompletion, self).__init__()
        self.model = model
        self.criterion = criterion
        self.metric = metric
        self.num_negative = num_negative
        self.margin = margin
        self.adversarial_temperature = adversarial_temperature
        self.strict_negative = strict_negative
        self.filtered_ranking = filtered_ranking
        self.fact_ratio = fact_ratio
        self.sample_weight = sample_weight

    def preprocess(self, train_set, valid_set, test_set):
        if isinstance(train_set, torch_data.Subset):
            dataset = train_set.dataset
        else:
            dataset = train_set
        self.num_entity = dataset.num_entity
        self.num_relation = dataset.num_relation
        self.register_buffer("graph", dataset.graph)
        fact_mask = torch.ones(len(dataset), dtype=torch.bool)
        fact_mask[valid_set.indices] = 0
        fact_mask[test_set.indices] = 0
        if self.fact_ratio:
            length = int(len(train_set) * self.fact_ratio)
            index = torch.randperm(len(train_set))[length:]
            train_indices = torch.tensor(train_set.indices)
            fact_mask[train_indices[index]] = 0
            train_set = torch_data.Subset(train_set, index)
        self.register_buffer("fact_graph", dataset.graph.edge_mask(fact_mask))

        if self.sample_weight:
            degree_hr = torch.zeros(self.num_entity, self.num_relation, dtype=torch.long)
            degree_tr = torch.zeros(self.num_entity, self.num_relation, dtype=torch.long)
            for h, t, r in train_set:
                degree_hr[h, r] += 1
                degree_tr[t, r] += 1
            self.register_buffer("degree_hr", degree_hr)
            self.register_buffer("degree_tr", degree_tr)

        return train_set, valid_set, test_set

    def forward(self, batch, all_loss=None, metric=None):
        """"""
        all_loss = torch.tensor(0, dtype=torch.float32, device=self.device)
        metric = {}

        pred = self.predict(batch, all_loss, metric)
        pos_h_index, pos_t_index, pos_r_index = batch.t()

        for criterion, weight in self.criterion.items():
            if criterion == "bce":
                target = torch.zeros_like(pred)
                target[:, 0] = 1
                loss = F.binary_cross_entropy_with_logits(pred, target, reduction="none")

                neg_weight = torch.ones_like(pred)
                if self.adversarial_temperature > 0:
                    with torch.no_grad():
                        neg_weight[:, 1:] = F.softmax(pred[:, 1:] / self.adversarial_temperature, dim=-1)
                else:
                    neg_weight[:, 1:] = 1 / self.num_negative
                loss = (loss * neg_weight).sum(dim=-1) / neg_weight.sum(dim=-1)
            elif criterion == "ce":
                target = torch.zeros(len(pred), dtype=torch.long, device=self.device)
                loss = F.cross_entropy(pred, target, reduction="none")
            elif criterion == "ranking":
                positive = pred[:, :1]
                negative = pred[:, 1:]
                target = torch.ones_like(negative)
                loss = F.margin_ranking_loss(positive, negative, target, margin=self.margin)
            else:
                raise ValueError("Unknown criterion `%s`" % criterion)

            if self.sample_weight:
                sample_weight = self.degree_hr[pos_h_index, pos_r_index] * self.degree_tr[pos_t_index, pos_r_index]
                sample_weight = 1 / sample_weight.float().sqrt()
                loss = (loss * sample_weight).sum() / sample_weight.sum()
            else:
                loss = loss.mean()

            name = tasks._get_criterion_name(criterion)
            metric[name] = loss
            all_loss += loss * weight

        return all_loss, metric

    def predict(self, batch, all_loss=None, metric=None):
        pos_h_index, pos_t_index, pos_r_index = batch.t()
        batch_size = len(batch)

        if all_loss is None:
            # test
            all_index = torch.arange(self.num_entity, device=self.device)
            t_preds = []
            h_preds = []
            for neg_index in all_index.split(self.num_negative):
                r_index = pos_r_index.unsqueeze(-1).expand(-1, len(neg_index))
                h_index, t_index = torch.meshgrid(pos_h_index, neg_index)
                t_pred = self.model(self.fact_graph, h_index, t_index, r_index)
                t_preds.append(t_pred)
            t_pred = torch.cat(t_preds, dim=-1)
            for neg_index in all_index.split(self.num_negative):
                r_index = pos_r_index.unsqueeze(-1).expand(-1, len(neg_index))
                t_index, h_index = torch.meshgrid(pos_t_index, neg_index)
                h_pred = self.model(self.fact_graph, h_index, t_index, r_index)
                h_preds.append(h_pred)
            h_pred = torch.cat(h_preds, dim=-1)
            pred = torch.stack([t_pred, h_pred], dim=1)
            # in case of GPU OOM
            pred = pred.cpu()
        else:
            # train
            if self.strict_negative:
                neg_index = self._strict_negative(pos_h_index, pos_t_index, pos_r_index)
            else:
                neg_index = torch.randint(self.num_entity, (batch_size, self.num_negative), device=self.device)
            h_index = pos_h_index.unsqueeze(-1).repeat(1, self.num_negative + 1)
            t_index = pos_t_index.unsqueeze(-1).repeat(1, self.num_negative + 1)
            r_index = pos_r_index.unsqueeze(-1).repeat(1, self.num_negative + 1)
            t_index[:batch_size // 2, 1:] = neg_index[:batch_size // 2]
            h_index[batch_size // 2:, 1:] = neg_index[batch_size // 2:]
            pred = self.model(self.fact_graph, h_index, t_index, r_index, all_loss=all_loss, metric=metric)

        return pred

    def target(self, batch):
        # test target
        pos_h_index, pos_t_index, pos_r_index = batch.t()
        target = torch.stack([pos_t_index, pos_h_index], dim=1)

        hr_index_set, hr_inverse = torch.unique(pos_h_index * self.num_relation + pos_r_index, return_inverse=True)
        tr_index_set, tr_inverse = torch.unique(pos_t_index * self.num_relation + pos_r_index, return_inverse=True)
        hr_index2id = -torch.ones(self.num_entity * self.num_relation, dtype=torch.long, device=self.device)
        hr_index2id[hr_index_set] = torch.arange(len(hr_index_set), device=self.device)
        tr_index2id = -torch.ones(self.num_entity * self.num_relation, dtype=torch.long, device=self.device)
        tr_index2id[tr_index_set] = torch.arange(len(tr_index_set), device=self.device)

        h_index, t_index, r_index = self.graph.edge_list.t()
        hr_index = h_index * self.num_relation + r_index
        tr_index = t_index * self.num_relation + r_index
        valid = hr_index2id[hr_index] >= 0
        hr_index = hr_index[valid]
        t_index = t_index[valid]
        t_mask_set = torch.ones(len(hr_index_set), self.num_entity, dtype=torch.bool, device=self.device)
        t_mask_set[hr_index2id[hr_index], t_index] = 0
        t_mask = t_mask_set[hr_inverse]
        valid = tr_index2id[tr_index] >= 0
        tr_index = tr_index[valid]
        h_index = h_index[valid]
        h_mask_set = torch.ones(len(tr_index_set), self.num_entity, dtype=torch.bool, device=self.device)
        h_mask_set[tr_index2id[tr_index], h_index] = 0
        h_mask = h_mask_set[tr_inverse]
        mask = torch.stack([t_mask, h_mask], dim=1)

        # in case of GPU OOM
        return mask.cpu(), target.cpu()

    def evaluate(self, pred, target):
        mask, target = target

        pos_pred = pred.gather(-1, target.unsqueeze(-1))
        if self.filtered_ranking:
            ranking = torch.sum((pos_pred <= pred) & mask, dim=-1) + 1
        else:
            ranking = torch.sum(pos_pred <= pred, dim=-1) + 1

        metric = {}
        for _metric in self.metric:
            if _metric == "mr":
                score = ranking.float().mean()
            elif _metric == "mrr":
                score = (1 / ranking.float()).mean()
            elif _metric.startswith("hits@"):
                threshold = int(_metric[5:])
                score = (ranking <= threshold).float().mean()
            else:
                raise ValueError("Unknown metric `%s`" % _metric)

            name = tasks._get_metric_name(_metric)
            metric[name] = score

        return metric

    def visualize(self, batch):
        h_index, t_index, r_index = batch.t()
        return self.model.visualize(self.fact_graph, h_index, t_index, r_index)

    @torch.no_grad()
    def _strict_negative(self, pos_h_index, pos_t_index, pos_r_index):
        batch_size = len(pos_h_index)

        hr_index_set, hr_inverse = torch.unique(pos_h_index * self.num_relation + pos_r_index, return_inverse=True)
        tr_index_set, tr_inverse = torch.unique(pos_t_index * self.num_relation + pos_r_index, return_inverse=True)
        hr_index2id = -torch.ones(self.num_entity * self.num_relation, dtype=torch.long, device=self.device)
        hr_index2id[hr_index_set] = torch.arange(len(hr_index_set), device=self.device)
        tr_index2id = -torch.ones(self.num_entity * self.num_relation, dtype=torch.long, device=self.device)
        tr_index2id[tr_index_set] = torch.arange(len(tr_index_set), device=self.device)

        h_index, t_index, r_index = self.fact_graph.edge_list.t()
        hr_index = h_index * self.num_relation + r_index
        tr_index = t_index * self.num_relation + r_index
        valid = hr_index2id[hr_index] >= 0
        hr_index = hr_index[valid]
        t_index = t_index[valid]
        t_mask_set = torch.ones(len(hr_index_set), self.num_entity, dtype=torch.bool, device=self.device)
        t_mask_set[hr_index2id[hr_index], t_index] = 0
        t_mask = t_mask_set[hr_inverse]
        valid = tr_index2id[tr_index] >= 0
        tr_index = tr_index[valid]
        h_index = h_index[valid]
        h_mask_set = torch.ones(len(tr_index_set), self.num_entity, dtype=torch.bool, device=self.device)
        h_mask_set[tr_index2id[tr_index], h_index] = 0
        h_mask = h_mask_set[tr_inverse]

        num_neg_t = t_mask.sum(dim=-1, keepdim=True)
        num_neg_h = h_mask.sum(dim=-1, keepdim=True)
        num_cum_neg_t = num_neg_t.cumsum(0)
        num_cum_neg_h = num_neg_h.cumsum(0)

        neg_t_index = t_mask.nonzero()[:, 1]
        neg_h_index = h_mask.nonzero()[:, 1]

        rand = torch.rand(batch_size, self.num_negative, device=self.device)
        index = (rand[:batch_size // 2] * num_neg_t[:batch_size // 2]).long()
        index = index + (num_cum_neg_t[:batch_size // 2] - num_neg_t[:batch_size // 2])
        neg_index_t = neg_t_index[index]

        index = (rand[batch_size // 2:] * num_neg_h[batch_size // 2:]).long()
        index = index + (num_cum_neg_h[batch_size // 2:] - num_neg_h[batch_size // 2:])
        neg_index_h = neg_h_index[index]

        neg_index = torch.cat([neg_index_t, neg_index_h])

        return neg_index