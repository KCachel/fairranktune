import random
import numpy as np

def CheckFull(item_ids, group_ids, phi):
    """
    Function to error check full input.
    :param item_ids: numpy array of ints representing item ids
    :param group_ids: numpy array of ints representing values in a protected attribute
    :param phi: float in range [0,1]
    :return: raise error if appropriate
    """

    if not isinstance(item_ids, np.ndarray):
        raise TypeError("Input item_ids must be ndarray")

    if not isinstance(group_ids, np.ndarray):
        raise TypeError("Input group_ids must be ndarray")

    if (np.min(np.unique(group_ids)) != 0) or (np.max(np.unique(group_ids)) != len(
            np.unique(group_ids)) - 1):  # check for consecutive group encodings in group ids
        raise ValueError("Please represent group ids via consecutive integers")

    if len(item_ids) != len(group_ids):  # check size of items and groups match
        raise ValueError("Please input a item and group array of same size")

    if len(set(item_ids)) != len(item_ids):  # check for repetition in item ids
        raise ValueError("Please input unique item ids")

    if phi > 1:  # check for phi < 1
        raise ValueError("Please input phi less than or equal to 1")

    if phi < 0:  # check for phi > 0
        raise ValueError("Please input phi greater than or equal to 0")


def CheckDistributions(group_proportions, num_items, phi):
    """
    Function to error check distribution input.
    :param item_ids: numpy array of ints representing item ids
    :param group_ids: numpy array of ints representing values in a protected attribute
    :param phi: float in range [0,1]
    :return: raise error if appropriate
    """
    if phi > 1:  # check for phi < 1
        raise ValueError("Please input phi less than or equal to 1")

    if phi < 0:  # check for phi > 0
        raise ValueError("Please input phi greater than or equal to 0")

    if np.sum(group_proportions) != 1:  # check group proportions sum to 1
        raise ValueError("Please input group proportions that sum to 1")

    if not isinstance(num_items, int):
        raise TypeError("Input num_items must be int")


def MakeRank(item_ids, group_ids, phi):
    """
    Core GenFromGroups data generation method.
        :param item_ids: numpy array of ints representing item ids
        :param group_ids: numpy array of ints representing values in a protected attribute
        :param phi: float in range [0,1]
        :return: resulting_ranking (numpy array of items ids ordered), ranking_group_ids (numpy array of group ids corresponding to resulting_ranking)
        """
    resulting_ranking = []


    unique_grp_ids, grp_count = np.unique(group_ids, return_counts=True)
    grp_proportion = grp_count / len(item_ids)  # proportion of total pool

    minority_index = np.argmin(grp_proportion)
    minority_proportion = np.min(grp_proportion)
    phi_scaled = ((phi - 0)/(1 - 0)) *(1 - minority_proportion)+minority_proportion
    #print("phi ",phi, "is phi scaled: ", phi_scaled) useful to understanding the scaling procedure
    grp_proportion = (grp_proportion/(np.sum(grp_proportion) - np.min(grp_proportion)))*(1-phi_scaled)
    grp_proportion[minority_index] = phi_scaled
    zipped = zip(grp_proportion, unique_grp_ids)

    items_in_each_group_id = [np.where(np.asarray(group_ids) == i)[0].tolist() for i in
                              unique_grp_ids]  # indexed by group_id #

    if phi == 1: #shuffle items in positions to add randomness (can comment out, without effecting metrics_
        for i in range(len(items_in_each_group_id)):
            random.shuffle(items_in_each_group_id[i])




    lows = np.zeros_like(unique_grp_ids, dtype= float)
    highs = np.zeros_like(unique_grp_ids, dtype = float)
    highs[-1] = 1 #last has to be 1

    #set the bounds of group proportions
    low_counter = 0
    for g in unique_grp_ids:
        lows[g] = low_counter
        upper_bound = low_counter + grp_proportion[g]
        highs[g] = upper_bound
        low_counter = upper_bound


    while all(grp_count > 0): # each group has items to place
        r = random.uniform(0, 1)
        grp_2_place = np.argwhere(np.bitwise_and(r > lows, r < highs) == True).flatten()[0]
        resulting_ranking.append(items_in_each_group_id[grp_2_place].pop())
        grp_count[grp_2_place] -= 1



    #place items in order of smallest to largest group
    while all(grp_count == 0) == False:
        grp_2_add = np.argwhere(grp_count == np.min(grp_count[np.nonzero(grp_count)])).flatten()[0]
        for i in range(0, grp_count[grp_2_add]):
            resulting_ranking.append(items_in_each_group_id[grp_2_add].pop())
            grp_count[grp_2_add] -= 1

    item_numpy = np.asarray(item_ids)
    ranking_group_ids = [group_ids[np.argwhere(item_numpy == i)[0][0]] for i in resulting_ranking]
    return np.asarray(resulting_ranking), np.asarray(ranking_group_ids)



def GenFromGroups(group_proportions, num_items, phi, r_cnt):
    """
    RankTune method with group proportions (as opposed to actual items).
    :param group_proportions: numpy array of group_proportions
    :param num_items: int for number of items to be ranked
    :param phi: float in range [0,1]
    :param r_cnt: int number of rankings to return
    :return: resulting_ranking (numpy array of items ids ordered x r_cnt), ranking_group_ids (numpy array of group ids corresponding to resulting_ranking x r_cnt)
)
    """
    CheckDistributions(group_proportions, num_items, phi)
    item_ids = np.arange(0, num_items)
    group_ids = np.empty(0, dtype = int)
    for g in range(0,len(group_proportions)):
        group_ids = np.hstack((group_ids, np.tile(int(g), int(num_items*group_proportions[g]))))

    items, groups = MakeRank(item_ids, group_ids, phi)
    for i in range(0,r_cnt - 1):
        items_next, groups_next = MakeRank(item_ids, group_ids, phi)
        items = np.column_stack((items, items_next))
        groups = np.column_stack((groups, groups_next))

    return items, groups

def ScoredGenFromGroups(group_proportions, num_items, phi, r_cnt, score_dist):
    """
    RankTune method with group proportions (as opposed to actual items), and random relevance scores assigned to items.
    :param group_proportions: numpy array of group_proportions
    :param num_items: int for number of items to be ranked
    :param phi: float in range [0,1]
    :param r_cnt: int number of rankings to return
    :param score_dist: string either "uniform" or "normal
    :return: resulting_ranking (list of items ids ordered x r_cnt), ranking_group_ids (list of group ids corresponding to resulting_ranking x r_cnt), scores (synthetic associated scores x r_cnt)
    """
    CheckDistributions(group_proportions, num_items, phi)
    item_ids = np.arange(0, num_items)
    group_ids = np.empty(0, dtype = int)
    for g in range(0,len(group_proportions)):
        group_ids = np.hstack((group_ids, np.tile(int(g), int(num_items*group_proportions[g]))))
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
    items, groups = MakeRank(item_ids, group_ids, phi)
    for i in range(0, r_cnt - 1):
        items_next, groups_next = MakeRank(item_ids, group_ids, phi)
        items = np.column_stack((items, items_next))
        groups = np.column_stack((groups, groups_next))

    return items, groups, scores

def GenFromItems(item_ids, group_ids, phi, r_cnt):
    """
    GenFromGroups method with actual items (as opposed to group proportions).
    :param item_ids: numpy array of ints representing item ids
    :param group_ids: numpy array of ints representing values in a protected attribute
    :param phi: float in range [0,1]
    :param r_cnt: int number of rankings to return
    :return: resulting_ranking (numpy array of items ids ordered x r_cnt), ranking_group_ids (numpy array of group ids corresponding to resulting_ranking x r_cnt)
    """
    CheckFull(item_ids, group_ids, phi)
    items, groups = MakeRank(item_ids, group_ids, phi)
    for i in range(0, r_cnt - 1):
        items_next, groups_next = MakeRank(item_ids, group_ids, phi)
        items = np.column_stack((items, items_next))
        groups = np.column_stack((groups, groups_next))

    return items, groups

def ScoredGenFromItems(item_ids, group_ids, phi, r_cnt, score_dist):
    """
    RankTune method with actual items (as opposed to group proportions), and random relevance scores assigned to items.
    :param item_ids: numpy array of ints representing item ids
    :param group_ids: numpy array of ints representing values in a protected attribute
    :param phi: float in range [0,1]
    :param r_cnt: int number of rankings to return
    :return: resulting_ranking (numpy array of items ids ordered x r_cnt), ranking_group_ids (numpy array of group ids corresponding to resulting_ranking x r_cnt)
    """
    CheckFull(item_ids, group_ids, phi)
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
    items, groups = MakeRank(item_ids, group_ids, phi)
    for i in range(0, r_cnt - 1):
        items_next, groups_next = MakeRank(item_ids, group_ids, phi)
        items = np.column_stack((items, items_next))
        groups = np.column_stack((groups, groups_next))

    return items, groups, scores