import pandas as pd
from FairRankTune.Metrics.ComboUtil import *

# Script to calculate Exposure-based metrics
# References: Singh, A., & Joachims, T. (2018, July). Fairness of exposure in rankings.
# In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (pp. 2219-2228).
# References: Diaz, F., Mitra, B., Ekstrand, M. D., Biega, A. J., & Carterette, B. (2020, October).
# Evaluating stochastic rankings with expected exposure.
# In Proceedings of the 29th ACM international conference on information & knowledge management (pp. 275-284).
# Raj, A., & Ekstrand, M. D. (2022, July). Measuring Fairness in Ranked Results: An Analytical and Empirical Comparison.
# In Proceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval (pp. 726-736).


def EXP(ranking_df, item_group_dict, combo):
    """
    Calculate group fairness of Exposure EXP (Singh et al. & Diaz et al.).
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param combo: String for the aggregation metric used in calculating the meta metric.
    :return: EXP value, Dictionary of group average exposure scores (groups are keys).
    """
    unique_grps, grp_count_items = np.unique(
        list(item_group_dict.values()), return_counts=True
    )
    num_items = len(list(item_group_dict.keys()))
    num_unique_rankings = len(ranking_df.columns)
    exp_vals = exp_at_position_array(num_items)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)

    for r in range(0, num_unique_rankings):
        single_ranking = ranking_df[ranking_df.columns[r]]  # isolate ranking
        single_ranking = np.array(
            single_ranking[~pd.isnull(single_ranking)]
        )  # drop any NaNs
        for i in range(0, len(single_ranking)):
            item = single_ranking[i]
            grp_of_item = item_group_dict[item]
            exp_of_item = exp_vals[i]
            # update total group exp
            grp_exposures[grp_of_item] += exp_of_item

    vals = grp_exposures / grp_count_items
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


def EXPU(ranking_df, item_group_dict, relevance_df, combo):
    """
    Calculate group fairness of Exposure Utility EXPU (Singh et al.).
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param relevance_df: Pandas dataframe of relevance scores associated with each item in ranking(s).
    :param combo: String for the aggregation metric used in calculating the meta metric.
    :return: EXPU value, Dictionary of group average exposure-utility scores (groups are keys).
    """
    unique_grps, grp_count_items = np.unique(
        list(item_group_dict.values()), return_counts=True
    )
    num_items = len(list(item_group_dict.keys()))
    num_unique_rankings = len(ranking_df.columns)
    exp_vals = exp_at_position_array(num_items)
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
        if np.any((assoc_rel < 0) | (assoc_rel > 1)):
            raise AssertionError(
                "Exposure Realized Utility requires that relevance score be between 0 (not relevant) or 1 (relevant)."
            )
        for i in range(0, len(single_ranking)):
            item = single_ranking[i]
            rel_of_item = assoc_rel[i]
            grp_of_item = item_group_dict[item]
            exp_of_item = exp_vals[i]
            # update total group exp
            grp_exposures[grp_of_item] += exp_of_item
            grp_relevances[grp_of_item] += rel_of_item

    avg_exp = grp_exposures / grp_count_items
    avg_utility = grp_relevances / grp_count_items
    vals = avg_exp / avg_utility
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


def EXPRU(ranking_df, item_group_dict, relevance_df, ctr_df, combo):
    """
    Calculate group fairness of Exposure Realized Utility EXPRU (Singh et al.).
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param relevance_df: Pandas dataframe of relevance scores associated with each item in ranking(s).
    :param ctr_df: Pandas dataframe of click-through-rates associated with each item in ranking(s).
    :param combo: String for the aggregation metric used in calculating the meta metric.
    :return: EXPRU value, Dictionary of group average exposure realized utility scores (groups are keys).
    """
    unique_grps, grp_count_items = np.unique(
        list(item_group_dict.values()), return_counts=True
    )
    num_unique_rankings = len(ranking_df.columns)
    grp_relevances = np.zeros_like(unique_grps, dtype=np.float64)
    grp_ctr = np.zeros_like(unique_grps, dtype=np.float64)

    for r in range(0, num_unique_rankings):
        single_ranking = ranking_df[ranking_df.columns[r]]  # isolate ranking
        single_ranking = np.array(
            single_ranking[~pd.isnull(single_ranking)]
        )  # drop any NaNs
        assoc_rel = relevance_df[
            relevance_df.columns[r]
        ]  # isolate reelvance score for this ranking
        assoc_rel = np.array(assoc_rel[~pd.isnull(assoc_rel)])  # drop any NaNs
        if np.any((assoc_rel < 0) | (assoc_rel > 1)):
            raise AssertionError(
                "Exposure Realized Utility requires that relevance score be between 0 (not relevant) or 1 (relevant)."
            )
        assoc_ctr = ctr_df[
            ctr_df.columns[r]
        ]  # isolate relevance score for this ranking
        assoc_ctr = np.array(assoc_ctr[~pd.isnull(assoc_ctr)])  # drop any NaNs
        if np.any((assoc_ctr < 0) | (assoc_ctr > 1)):
            raise AssertionError(
                "Exposure Realized Utility requires that click through rate be between 0 (no clicks) or 1 (100% ctr). "
            )
        for i in range(0, len(single_ranking)):
            item = single_ranking[i]
            rel_of_item = assoc_rel[i]
            grp_of_item = item_group_dict[item]
            ctr_of_item = assoc_ctr[i]
            # update total group exp
            grp_ctr[grp_of_item] += ctr_of_item
            grp_relevances[grp_of_item] += rel_of_item

    avg_ctr = grp_ctr / grp_count_items
    avg_utility = grp_relevances / grp_count_items
    vals = avg_ctr / avg_utility
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


def exp_at_position_array(num_items):
    """
    Function to calculate the exposure associated with each position in the ranking.
    :param num_items: Int, number of items to be ranked.
    :return: Numpy array of exposure associated with each position.
    """
    return np.array([(1 / (np.log2(i + 1))) for i in range(1, num_items + 1)])
