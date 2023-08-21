import random
import numpy as np
import pandas as pd


def __CheckFull(phi):
    """
    Function to error check phi parameter.
    :param phi: Float in range [0,1].
    :return: Raise error if appropriate.
    """
    if phi > 1:  # check for phi < 1
        raise ValueError("Please input phi less than or equal to 1")

    if phi < 0:  # check for phi > 0
        raise ValueError("Please input phi greater than or equal to 0")


def __CheckDistributions(group_proportions, num_items, phi):
    """
    Function to error check distribution input.
    :param item_ids: Numpy array of ints representing item ids.
    :param group_ids: Numpy array of ints representing values in a protected attribute.
    :param phi: Float in range [0,1].
    :return: Raise error if appropriate.
    """
    if phi > 1:  # check for phi < 1
        raise ValueError("Please input phi less than or equal to 1")

    if phi < 0:  # check for phi > 0
        raise ValueError("Please input phi greater than or equal to 0")

    if np.sum(group_proportions) != 1:  # check group proportions sum to 1
        raise ValueError("Please input group proportions that sum to 1")

    if not isinstance(num_items, int):
        raise TypeError("Input num_items must be int")


def __MakeRank(item_ids, group_ids, phi):
    """
    Function for core RankTune fairness-aware ranked list generation.
    :param item_ids: Numpy array of item ids.
    :param group_ids: Numpy array of corresponding group ids.
    :param phi: Float, Representativeness in range [0,1]; where 0 is unfair and 1 is most fair and representative.
    :return: Numpy array of items (i.e., generated ranking).
    """
    resulting_ranking = []

    unique_grp_ids, grp_count = np.unique(group_ids, return_counts=True)
    grp_proportion = grp_count / len(item_ids)  # proportion of total pool

    minority_index = np.argmin(grp_proportion)
    minority_proportion = np.min(grp_proportion)
    phi_scaled = (1 - phi) * (1 - minority_proportion) + minority_proportion
    grp_proportion = (
        grp_proportion / (np.sum(grp_proportion) - np.min(grp_proportion))
    ) * (1 - phi_scaled)

    grp_proportion[minority_index] = phi_scaled
    items_in_each_group_id = [
        item_ids[np.where(np.asarray(group_ids) == i)[0].tolist()].tolist()
        for i in unique_grp_ids
    ]  # indexed by group_id #

    if phi == 0:  # shuffle items in positions to add randomness
        for i in range(len(items_in_each_group_id)):
            random.shuffle(items_in_each_group_id[i])

    lows = np.zeros_like(unique_grp_ids, dtype=float)
    highs = np.zeros_like(unique_grp_ids, dtype=float)
    highs[-1] = 1  # last has to be 1

    # set the bounds of group proportions
    low_counter = 0
    for g in range(0, len(unique_grp_ids)):
        lows[g] = low_counter
        upper_bound = low_counter + grp_proportion[g]
        highs[g] = upper_bound
        low_counter = upper_bound

    while all(grp_count > 0):  # each group has items to place
        r = random.uniform(0, 1)
        grp_2_place = np.argwhere(
            np.bitwise_and(r > lows, r < highs) == True
        ).flatten()[0]
        resulting_ranking.append(items_in_each_group_id[grp_2_place].pop())
        grp_count[grp_2_place] -= 1

    # place items in order of smallest to largest group
    while all(grp_count == 0) == False:
        grp_2_add = np.argwhere(
            grp_count == np.min(grp_count[np.nonzero(grp_count)])
        ).flatten()[0]
        for i in range(0, grp_count[grp_2_add]):
            resulting_ranking.append(items_in_each_group_id[grp_2_add].pop())
            grp_count[grp_2_add] -= 1

    item_numpy = np.asarray(item_ids)
    # ranking_group_ids = [group_ids[np.argwhere(item_numpy == i)[0][0]] for i in resulting_ranking]
    return np.asarray(resulting_ranking)


def GenFromGroups(group_proportions, num_items, phi, r_cnt):
    """
    RankTune method generating data from group proportions (as opposed to actual items).
    :param group_proportions: Numpy array of group_proportions.
    :param num_items: Int, number of items in ranking(s).
    :param phi: Float, Representativeness in range [0,1]; where 0 is unfair and 1 is most fair and representative.
    :param r_cnt: Int, number of rankings to generate.
    :return: ranking_df - Pandas dataframe of generated ranking(s),  item_group_dict -  Dictionary of items (keys) and their group membership (values).
    """
    __CheckDistributions(group_proportions, num_items, phi)
    item_ids = np.arange(0, num_items)
    group_ids = np.empty(0, dtype=int)
    for g in range(0, len(group_proportions)):
        group_ids = np.hstack(
            (group_ids, np.tile(int(g), int(num_items * group_proportions[g])))
        )

    # Make item_group_dict
    item_group_dict = dict(zip(item_ids.tolist(), group_ids.tolist()))

    items = __MakeRank(item_ids, group_ids, phi)
    for i in range(0, r_cnt - 1):
        items_next = __MakeRank(item_ids, group_ids, phi)
        items = np.column_stack((items, items_next))

    ranking_df = pd.DataFrame(items)
    return ranking_df, item_group_dict


def ScoredGenFromGroups(group_proportions, num_items, phi, r_cnt, score_dist, seed):
    """
    RankTune method generating data from group proportions (as opposed to actual items), and random relevance scores assigned to items.
    :param group_proportions: Numpy array of group_proportions.
    :param num_items: Int, number of items in ranking(s).
    :param phi: Float, Representativeness in range [0,1]; where 0 is unfair and 1 is most fair and representative.
    :param r_cnt: Int, number of rankings to generate.
    :param score_dist: String, either "uniform" or "normal for generating scores.
    :param seed: Random seed value for reproducibility.
    :return: ranking_df - Pandas dataframe of generated ranking(s),  item_group_dict -  Dictionary of items (keys) and their group membership (values), scores-df - Pandas dataframe of generates scores.
    """
    __CheckDistributions(group_proportions, num_items, phi)
    item_ids = np.arange(0, num_items)
    group_ids = np.empty(0, dtype=int)
    np.random.seed(seed)  # for reproducibility
    for g in range(0, len(group_proportions)):
        group_ids = np.hstack(
            (group_ids, np.tile(int(g), int(num_items * group_proportions[g])))
        )

    # Make item_group_dict
    item_group_dict = dict(zip(item_ids.tolist(), group_ids.tolist()))
    if score_dist == "normal":
        scores = np.random.standard_normal(size=len(item_ids))
        for i in range(0, r_cnt - 1):
            scores_next = np.random.standard_normal(size=len(item_ids))
            scores = np.column_stack((scores, scores_next))
    elif score_dist == "uniform":
        scores = np.random.uniform(0, 1, size=len(item_ids))
        for i in range(0, r_cnt - 1):
            scores_next = np.random.uniform(0, 1, size=len(item_ids))
            scores = np.column_stack((scores, scores_next))
    items = __MakeRank(item_ids, group_ids, phi)
    for i in range(0, r_cnt - 1):
        items_next = __MakeRank(item_ids, group_ids, phi)
        items = np.column_stack((items, items_next))

    ranking_df = pd.DataFrame(items)
    scores_df = pd.DataFrame(scores)
    return ranking_df, item_group_dict, scores_df


def GenFromItems(item_group_dict, phi, r_cnt):
    """
    RankTune method generating data from known items with group membership.
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param num_items: Int, number of items in ranking(s).
    :param phi: Float, Representativeness in range [0,1]; where 0 is unfair and 1 is most fair and representative.
    :param r_cnt: Int, number of rankings to generate.
    :return: ranking_df - Pandas dataframe of generated ranking(s),  item_group_dict -  Dictionary of items (keys) and their group membership (values), scores-df - Pandas dataframe of generates scores.
    """
    __CheckFull(phi)
    item_ids = list(item_group_dict.keys())
    group_ids = np.asarray([item_group_dict[i] for i in item_ids])

    items = __MakeRank(np.asarray(item_ids), group_ids, phi)
    for i in range(0, r_cnt - 1):
        items_next = __MakeRank(np.asarray(item_ids), group_ids, phi)
        items = np.column_stack((items, items_next))

    ranking_df = pd.DataFrame(items)
    return ranking_df, item_group_dict


def ScoredGenFromItems(item_group_dict, phi, r_cnt, score_dist, seed):
    """
    RankTune method generating data from known items with group membership, and random relevance scores assigned to items.
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param num_items: Int, number of items in ranking(s).
    :param phi: Float, Representativeness in range [0,1]; where 0 is unfair and 1 is most fair and representative.
    :param r_cnt: Int, number of rankings to generate.
    :param score_dist: String, either "uniform" or "normal for generating scores.
    :param seed: Random seed value for reproducibility.
    :return: ranking_df - Pandas dataframe of generated ranking(s),  item_group_dict -  Dictionary of items (keys) and their group membership (values), scores-df - Pandas dataframe of generates scores.
    """
    __CheckFull(phi)
    item_ids = list(item_group_dict.keys())
    group_ids = np.asarray([item_group_dict[i] for i in item_ids])
    np.random.seed(seed)  # for reproducibility
    if score_dist == "normal":
        scores = np.random.standard_normal(size=len(item_ids))
        for i in range(0, r_cnt - 1):
            scores_next = np.random.standard_normal(size=len(item_ids))
            scores = np.column_stack((scores, scores_next))
    elif score_dist == "uniform":
        scores = np.random.uniform(0, 1, size=len(item_ids))
        for i in range(0, r_cnt - 1):
            scores_next = np.random.uniform(0, 1, size=len(item_ids))
            scores = np.column_stack((scores, scores_next))
    items = __MakeRank(np.asarray(item_ids), group_ids, phi)
    for i in range(0, r_cnt - 1):
        items_next = __MakeRank(np.asarray(item_ids), group_ids, phi)
        items = np.column_stack((items, items_next))

    ranking_df = pd.DataFrame(items)
    scores_df = pd.DataFrame(scores)
    return ranking_df, item_group_dict, scores_df
