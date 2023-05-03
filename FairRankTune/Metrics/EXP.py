import numpy as np
from FairRankTune.Metrics.ComboUtil import *
# Script to calculate Ecposure metric
# References: Singh, A., & Joachims, T. (2018, July). Fairness of exposure in rankings.
# In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (pp. 2219-2228).
def EXP(ranking, group_ids, combo):
    """
    Calculate EXP score (Singh et. al)
    :param ranking: Numpy array of ranking methods
    :param group_ids: Numpy array of group ids
    :param combo: String aggregation metric for calculating meta metric
    :return: EXP value, numpy array of group average exposure
    """
    unique_grps, grp_count_items = np.unique(group_ids, return_counts=True)
    num_items = len(ranking)
    exp_vals = exp_at_position_array(num_items)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)
    for i in range(0,num_items):
        grp_of_item = group_ids[i]
        exp_of_item = exp_vals[i]
        #update total group exp
        grp_exposures[grp_of_item] += exp_of_item

    vals = grp_exposures / grp_count_items
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

def exp_at_position_array(num_items):
    return np.array([(1/(np.log2(i+1))) for i in range(1,num_items+1)])