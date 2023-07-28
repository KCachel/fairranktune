import numpy as np
from FairRankTune.Metrics.ComboUtil import *
# Script to calculate Exposure Rank Based Precision metrics
# References: Kirnap, Ö., Diaz, F., Biega, A.J., Ekstrand, M.D., Carterette, B., & Yilmaz, E. (2021).
# Estimation of Fair Ranking Metrics with Incomplete Judgments. Proceedings of the Web Conference 2021.
def ERBE(ranking, group_ids, combo, decay):
    """
    Calculate Exposure (based on RBP) score (Kirnap et. al) and measure parity (equality); where the exposure should be equal for
each group.
    :param ranking: Numpy array of ranking methods
    :param group_ids: Numpy array of group ids
    :param combo: String aggregation metric for calculating meta metric
    :return: ERBE value, numpy array of group exposure equality (RBP-based)
    """
    unique_grps, grp_count_items = np.unique(group_ids, return_counts=True)
    num_items = len(ranking)
    exp_vals = exp_rbp_at_position_array(num_items, decay)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)
    for i in range(0,num_items):
        grp_of_item = group_ids[i]
        exp_of_item = exp_vals[i]
        #update total group exp
        grp_exposures[grp_of_item] += exp_of_item

    vals = (1 - decay)*grp_exposures
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


def ERBP(ranking, group_ids, combo, decay):
    """
    Calculate Exposure (based on RBP) score (Kirnap et. al) and measure proportionality; where the exposure should be proportional to the number of
items in the corpus that belong to a given group.
    :param ranking: Numpy array of ranking methods
    :param group_ids: Numpy array of group ids
    :param combo: String aggregation metric for calculating meta metric
    :return: ERBP value, numpy array of group exposure proportionality (RBP-based)
    """
    unique_grps, grp_count_items = np.unique(group_ids, return_counts=True)
    num_items = len(ranking)
    exp_vals = exp_rbp_at_position_array(num_items, decay)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)
    for i in range(0,num_items):
        grp_of_item = group_ids[i]
        exp_of_item = exp_vals[i]
        #update total group exp
        grp_exposures[grp_of_item] += exp_of_item

    vals = ((1 - decay)*grp_exposures)/ grp_count_items
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


def ERBR(ranking, group_ids, relevance, decay, combo,):
    """
    Calculate Exposure (based on RBP) score (Kirnap et. al) and measure proportionality to the relevance; here the exposure should be proportional to the number of items belonging to a given group that are relevant to the ranking
query
    :param ranking: Numpy array of ranking methods
    :param group_ids: Numpy array of group ids
    :param relvance: Numpy array of relevance values for items
    :param combo: String aggregation metric for calculating meta metric
    :return: ERBR value, numpy array of group exposure proportionality (RBP-based)
    """
    if np.any((relevance != 0) | (relevance != 1)):
        assert("Exposure (RBP) proportioanl to relevance requires relevance score to be either 0 (not relevant) or 1 (relevant). ")

    unique_grps, grp_count_items = np.unique(group_ids, return_counts=True)
    num_items = len(ranking)
    exp_vals = exp_rbp_at_position_array(num_items, decay)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)
    grp_relevance_cnt = np.zeros_like(unique_grps, dtype=np.float64)
    for i in range(0, num_items):
        grp_of_item = group_ids[i]
        exp_of_item = exp_vals[i]
        rel_of_item = relevance[i]
        # update total group exp
        grp_exposures[grp_of_item] += exp_of_item
        grp_relevance_cnt[grp_of_item] += rel_of_item

    vals = ((1 - decay) * grp_exposures) / grp_relevance_cnt
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


def exp_rbp_at_position_array(num_items, decay):
    return np.array([decay**(i - 1) for i in range(1,num_items+1)])