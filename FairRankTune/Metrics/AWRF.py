import numpy as np
from FairRankTune.Metrics.AggUtil import *
# Script to calculate AWRF metric
# References: Sapiezynski, P., Zeng, W., E Robertson, R., Mislove, A., & Wilson, C. (2019, May).
# Quantifying the impact of user attentionon fair group representation in ranked lists.
# In Companion proceedings of the 2019 world wide web conference (pp. 553-562).
# Ghosh, A., Dutt, R., & Wilson, C. (2021, July). When fair ranking meets uncertain inference.
# In Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval (pp. 1033-1043).


def AWRF(ranking, group_ids, p, combo):
    """
    Calculate AWRP score (Sapiezynski et al.)
    :param ranking: Numpy array of ranking methods
    :param group_ids: Numpy array of group ids
    :param p: p discounting param
    :param combo: String aggregation metric for calculating meta metric
    :return: AWRP score val, numpy array of group average attention
    """

    unique_grps, grp_count_items = np.unique(group_ids, return_counts=True)
    num_items = len(ranking)
    attn_vals = attention_vector(num_items, p)
    grp_attn_vals = np.zeros_like(unique_grps, dtype=np.float64)
    for i in range(0,num_items):
        grp_of_item = group_ids[i]
        attn_of_item = attn_vals[i]
        #update total group attention
        grp_attn_vals[grp_of_item] += attn_of_item

    vals = grp_attn_vals / grp_count_items

    if combo == 'MinMaxRatio':
        return MinMaxRatio(vals), vals
    if combo == 'MaxMinRatio':
        return MaxMinRatio(vals), vals
    if combo == 'MaxMinDiff':
        return MaxMinDiff(vals), vals
    if combo == 'MaxAbsDiff':
        return MaxAbsDiff(vals), vals
    if combo == 'MeanAbsDev':
        return MeanAbsDev(vals), vals
    if combo == 'LTwo':
        return LTwo(vals), vals
    if combo == 'Variance':
        return Variance(vals), vals

def attention_vector(num_items, p):
    return np.array([100*((1-p)**(k - 1))*p for k in range(1,num_items+1)])
