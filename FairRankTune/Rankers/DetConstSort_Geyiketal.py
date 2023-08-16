import numpy as np
import math
from collections import defaultdict as ddict


# References: Geyik, S. C., Ambler, S., & Kenthapadi, K. (2019, July).
# Fairness-aware ranking in search & recommendation systems with application to linkedin talent search.
# In Proceedings of the 25th acm sigkdd international conference on knowledge discovery & data mining (pp. 2221-2231).
import pandas as pd


def DETCONSTSORT(
    current_ranking_df, item_group_dict, current_ranking_scores_df, distribution, k
):
    """
    DetConstSort reranking algorithm.
    :param current_ranking_df: Pandas dataframe of ranking to be reranked.
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param current_ranking_scores_df: Pandas dataframe of relevance scores associated with each item in the ranking.
    :param distribution: Numpy array of the target distribution "p" in the paper. Ex. [.5, .5] is a fifty-fifty split.
    :param k: Int, how long the returned ranking should be.
    :return: reranking, Pandas dataframe of items,item_group_reranked_dict, dictionary of items and group membership,  Pandas dataframe  of scores for reranking,
    """

    # Convert dataframes to numpy arrays
    current_ranking = current_ranking_df[0].to_numpy()
    current_group_ids = np.asarray([item_group_dict[i] for i in current_ranking])
    current_ranking_scores = current_ranking_scores_df[0].to_numpy()

    # score_list is <group id>  <score> and <rank> <startrank> <id>
    score_list = [
        (
            current_group_ids[i],
            current_ranking_scores[i],
            i + 1,
            i + 1,
            current_ranking[i],
        )
        for i in range(len(current_ranking))
    ]

    unique_group_ids = list(np.unique(current_group_ids))
    AttrScores = {}
    num_items_per_group = {}
    min_grp_count = {}
    GlobalAttrCounts = {}
    constructed_ranking_group_ids = {}  # []
    rankedScoreList = {}  # []
    maxIndices = {}  # []
    last_empty_indx = 0
    k_iter = 0

    for grp_id in unique_group_ids:
        num_items_per_group[grp_id] = 0
        min_grp_count[grp_id] = 0
        GlobalAttrCounts[grp_id] = sum([1 for elem in score_list if elem[0] == grp_id])
        AttrScores[grp_id] = [
            (item[1], item[0], item[2], item[3], item[4])
            for item in score_list
            if item[0] == grp_id
        ]  # to be initialized

    while last_empty_indx <= k:
        if last_empty_indx == len(score_list):
            break

        k_iter += 1
        temp_min_attr_count_for_curr_prefix = ddict(int)
        changedMins = {}
        for grp_id in unique_group_ids:
            temp_min_attr_count_for_curr_prefix[grp_id] = math.floor(
                k_iter * distribution[grp_id]
            )
            if (
                min_grp_count[grp_id] < temp_min_attr_count_for_curr_prefix[grp_id]
                and min_grp_count[grp_id] < GlobalAttrCounts[grp_id]
            ):
                changedMins[grp_id] = AttrScores[grp_id][num_items_per_group[grp_id]]

        if len(changedMins) != 0:
            ordChangedMins = sorted(
                changedMins.items(), key=lambda x: x[1][0], reverse=True
            )
            for item in ordChangedMins:
                constructed_ranking_group_ids[last_empty_indx] = item[0]
                rankedScoreList[last_empty_indx] = item[1]
                maxIndices[last_empty_indx] = k_iter
                start = last_empty_indx
                while (
                    start > 0
                    and maxIndices[start - 1] >= start
                    and rankedScoreList[start - 1][0] < rankedScoreList[start][0]
                ):
                    swap(rankedScoreList, start - 1, start)
                    swap(maxIndices, start - 1, start)
                    swap(constructed_ranking_group_ids, start - 1, start)
                    start -= 1
                num_items_per_group[item[0]] += 1
                last_empty_indx += 1
            min_grp_count = dict(temp_min_attr_count_for_curr_prefix)

    K_items = []
    K_scores = []

    for i in range(0, k):
        item = rankedScoreList[i]
        K_items.append(int(item[4]))
        K_scores.append(item[0])

    reranking = np.asarray(K_items)
    reranking_scores = np.asarray(K_scores)
    current_rank = list(current_ranking)
    reranking_ids = np.asarray(
        [current_group_ids[current_rank.index(item)] for item in reranking]
    )
    item_group_reranked_dict = dict(zip(reranking, reranking_ids))
    return (
        pd.DataFrame(reranking),
        item_group_reranked_dict,
        pd.DataFrame(reranking_scores),
    )


def getdist(p):
    d = {}
    for item in p:
        if item["g"] not in d:
            d[item["g"]] = 1
        else:
            d[item["g"]] += 1
    for a in d:
        d[a] = d[a] / len(p)
    return d


def swap(temp_list, pos_i, pos_j):
    temp = temp_list[pos_i]
    temp_list[pos_i] = temp_list[pos_j]
    temp_list[pos_j] = temp
