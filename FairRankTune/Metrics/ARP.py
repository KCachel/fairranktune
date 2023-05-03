from FairRankTune.Metrics.ComboUtil import *
# Script to calculate ARP metric, using Cachel et al implementation
# Code References:  https://github.com/KCachel/MANI-Rank/blob/main/multi_fair/metrics.py
# References: Cachel, K., Rundensteiner, E., & Harrison, L. (2022, May). Mani-rank: Multiple attribute and intersectional group fairness for consensus ranking.
# In 2022 IEEE 38th International Conference on Data Engineering (ICDE) (pp. 1124-1137). IEEE.

def fpr(ranking, grp_mem):
    """   Compute the Favored Pair Representation of each group in the encoded attribute.
    :param ranking: A numpy array of ranking ids
    :param group_key: A numpy array of group ids
    :return fpr: python list of fpr score for each group (indexed by group id)"""
    # candidates = group_key[0]
    # grp_mem = group_key[1]
    num_groups = len(np.unique(grp_mem))
    r_list = list(ranking)
    #groups_of_candidates = candidates_by_group(candidates, grp_mem)
    groups_of_candidates = candidates_by_group(ranking, grp_mem)
    fpr = []
    pair_cnt = pair_count_at_position_array(len(ranking))
    pairs_in_ranking = pair_count(len(ranking))

    for i in range(0,num_groups):
        cands = groups_of_candidates[i]
        grp_sz = len(cands)
        total_favored = int(0)
        for x in cands:
            indx_in_r = r_list.index(x)
            favored_pairs_at_pos = pair_cnt[indx_in_r]
            total_favored += int(favored_pairs_at_pos)
        #numerator
        favored_over_other_grp = total_favored - pair_count(grp_sz)
        #print("numerator in parity : ",favored_over_other_grp)
        #denominator
        total_mixed_with_group = grp_sz*(len(ranking) - grp_sz)
        fpr.append(favored_over_other_grp/total_mixed_with_group)
        #print("denominator in parity: ", total_mixed_with_group)
    return fpr


def ARP(ranking, group_ids, combo):
    """
    Calculate ARP score
    :param ranking: Numpy array of ranking methods
    :param group_ids: Numpy array of group ids
    :param combo: String aggregation metric for calculating meta metric
    :return: ARP value, numpy array of FPR values
    """
    vals = np.asarray(fpr(ranking, group_ids))
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

def pair_count(num_candidates):
    return (num_candidates*(num_candidates - 1))/2

def candidates_by_group(candidates, grp_mem):
    """Create dictionary with key = group id and value = candidate ids
    ints instead of strings"""
    group_id_dict = {}
    for var in np.unique(grp_mem):
        idx = np.where(grp_mem == var)
        group_id_dict[(var)] = [item for item in candidates[idx].tolist()]  # make it a list of int
    return group_id_dict


def pair_count_at_position_array(num_candidates):
    return list(np.arange(num_candidates - 1, -1, -1))
