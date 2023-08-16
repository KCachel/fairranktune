import pandas as pd
from FairRankTune.Metrics.ComboUtil import *


# Script to calculate Exposure Rank Based Precision metrics
# References: Kirnap, Ö., Diaz, F., Biega, A.J., Ekstrand, M.D., Carterette, B., & Yilmaz, E. (2021).
# Estimation of Fair Ranking Metrics with Incomplete Judgments. Proceedings of the Web Conference 2021.
def ERBE(ranking_df, item_group_dict, decay, combo):
    """
    Calculate Exposure Rank Based Precision Equality ERBE; where exposure should be equal for each group (Kirnap et al.).
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param decay: Float, decay parameter for exposure based on the rank based precision metric.
    :param combo: String for the aggregation metric used in calculating the meta metric.
    :return: ERBE value, Dictionary of group RBP-based exposures (groups are keys).
    """

    unique_grps, grp_count_items = np.unique(
        list(item_group_dict.values()), return_counts=True
    )
    num_unique_rankings = len(ranking_df.columns)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)

    for r in range(0, num_unique_rankings):
        single_ranking = ranking_df[ranking_df.columns[r]]  # isolate ranking
        single_ranking = np.array(
            single_ranking[~pd.isnull(single_ranking)]
        )  # drop any NaNs
        exp_vals = exp_rbp_at_position_array(len(single_ranking), decay)
        for i in range(0, len(single_ranking)):
            item = single_ranking[i]
            grp_of_item = item_group_dict[item]
            exp_of_item = exp_vals[i]
            # update total group exp
            grp_exposures[grp_of_item] += exp_of_item

    Exposure_g = (1 - decay) * grp_exposures  # Eq. 2 in Kirnap et al.
    vals = Exposure_g
    if combo == "MinMaxRatio":
        return MinMaxRatio(vals), dict(zip(unique_grps, vals))
    if combo == "MaxMinRatio":
        return MaxMinRatio(vals), dict(zip(unique_grps, vals))
    if combo == "MaxMinDiff":
        return MaxMinDiff(vals), dict(zip(unique_grps, vals))
    if combo == "MaxAbsDiff":
        return MaxAbsDiff(vals), dict(zip(unique_grps, vals))
    if combo == "MeanAbsDev":
        return MeanAbsDev(vals), dict(zip(unique_grps, vals))
    if combo == "LTwo":
        return LTwo(vals), dict(zip(unique_grps, vals))
    if combo == "Variance":
        return Variance(vals), dict(zip(unique_grps, vals))


def ERBP(ranking_df, item_group_dict, decay, combo):
    """
    Calculate Exposure Rank Based Precision Proportionality ERBP; where exposure should be proportional to group size for each group (Kirnap et al.).
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param decay: Float, decay parameter for exposure based on the rank based precision metric.
    :param combo: String for the aggregation metric used in calculating the meta metric.
    :return: ERBP value, Dictionary of group RBP-based exposures (groups are keys).
    """
    unique_grps, grp_count_items = np.unique(
        list(item_group_dict.values()), return_counts=True
    )
    num_unique_rankings = len(ranking_df.columns)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)

    for r in range(0, num_unique_rankings):
        single_ranking = ranking_df[ranking_df.columns[r]]  # isolate ranking
        single_ranking = np.array(
            single_ranking[~pd.isnull(single_ranking)]
        )  # drop any NaNs
        exp_vals = exp_rbp_at_position_array(len(single_ranking), decay)
        for i in range(0, len(single_ranking)):
            item = single_ranking[i]
            grp_of_item = item_group_dict[item]
            exp_of_item = exp_vals[i]
            # update total group exp
            grp_exposures[grp_of_item] += exp_of_item

    Exposure_g = (1 - decay) * grp_exposures  # Eq. 2 in Kirnap et al.
    vals = Exposure_g / grp_count_items

    if combo == "MinMaxRatio":
        return MinMaxRatio(vals), dict(zip(unique_grps, vals))
    if combo == "MaxMinRatio":
        return MaxMinRatio(vals), dict(zip(unique_grps, vals))
    if combo == "MaxMinDiff":
        return MaxMinDiff(vals), dict(zip(unique_grps, vals))
    if combo == "MaxAbsDiff":
        return MaxAbsDiff(vals), dict(zip(unique_grps, vals))
    if combo == "MeanAbsDev":
        return MeanAbsDev(vals), dict(zip(unique_grps, vals))
    if combo == "LTwo":
        return LTwo(vals), dict(zip(unique_grps, vals))
    if combo == "Variance":
        return Variance(vals), dict(zip(unique_grps, vals))


def ERBR(ranking_df, item_group_dict, relevance_df, decay, combo):
    """
    Calculate Exposure Rank Based Precision Proportional to Relevance ERBR; where exposure should be proportional to group relevance for each group (Kirnap et al.).
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param relevance_df: Pandas dataframe of relevance scores associated with each item in ranking(s).
    :param decay: Float, decay parameter for exposure based on the rank based precision metric.
    :param combo: String for the aggregation metric used in calculating the meta metric.
    :return: ERBR value, Dictionary of group RBP-based exposures (groups are keys).
    """

    unique_grps, grp_count_items = np.unique(
        list(item_group_dict.values()), return_counts=True
    )
    num_unique_rankings = len(ranking_df.columns)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)
    grp_relevances = np.zeros_like(unique_grps, dtype=np.float64)

    for r in range(0, num_unique_rankings):
        single_ranking = ranking_df[ranking_df.columns[r]]  # isolate ranking
        single_ranking = np.array(
            single_ranking[~pd.isnull(single_ranking)]
        )  # drop any NaNs
        assoc_rel = relevance_df[
            relevance_df.columns[r]
        ]  # isolate reelvance score for this ranking
        assoc_rel = np.array(assoc_rel[~pd.isnull(assoc_rel)])  # drop any NaNs
        if np.any((assoc_rel != 0) | (assoc_rel != 1)):
            assert "Exposure Rank Based Precision Proportional to Relevance (ERBR) requires relevance scores to be either 0 (not relevant) or 1 (relevant). "
        exp_vals = exp_rbp_at_position_array(len(single_ranking), decay)
        for i in range(0, len(single_ranking)):
            item = single_ranking[i]
            rel_of_item = assoc_rel[i]
            grp_of_item = item_group_dict[item]
            exp_of_item = exp_vals[i]
            # update total group exp
            grp_exposures[grp_of_item] += exp_of_item
            grp_relevances[grp_of_item] += rel_of_item

    Exposure_g = (1 - decay) * grp_exposures  # Eq. 2 in Kirnap et al.
    vals = Exposure_g / grp_relevances
    if combo == "MinMaxRatio":
        return MinMaxRatio(vals), dict(zip(unique_grps, vals))
    if combo == "MaxMinRatio":
        return MaxMinRatio(vals), dict(zip(unique_grps, vals))
    if combo == "MaxMinDiff":
        return MaxMinDiff(vals), dict(zip(unique_grps, vals))
    if combo == "MaxAbsDiff":
        return MaxAbsDiff(vals), dict(zip(unique_grps, vals))
    if combo == "MeanAbsDev":
        return MeanAbsDev(vals), dict(zip(unique_grps, vals))
    if combo == "LTwo":
        return LTwo(vals), dict(zip(unique_grps, vals))
    if combo == "Variance":
        return Variance(vals), dict(zip(unique_grps, vals))


def exp_rbp_at_position_array(num_items, decay):
    """
    Determine the exposure (based on Rank Based Precision) value associate with each position.
    :param num_items: Int, number of items being ranked.
    :param decay: Float, decay parameter for exposure based on the rank based precision metric.
    :return: Numpy array of exposure values.
    """
    return np.array([decay ** (i - 1) for i in range(1, num_items + 1)])
