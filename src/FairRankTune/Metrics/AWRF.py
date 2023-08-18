import pandas as pd
from FairRankTune.Metrics.ComboUtil import *

# Script to calculate AWRF metric
# References: Sapiezynski, P., Zeng, W., E Robertson, R., Mislove, A., & Wilson, C. (2019, May).
# Quantifying the impact of user attention on fair group representation in ranked lists.
# In Companion proceedings of the 2019 world wide web conference (pp. 553-562).
# Ghosh, A., Dutt, R., & Wilson, C. (2021, July). When fair ranking meets uncertain inference.
# In Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval (pp. 1033-1043).


def AWRF(ranking_df, item_group_dict, p, combo):
    """
    Calculate group fairness of attention AWRF (Sapiezynski et al.).
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param p: Float, proportion of attention provided to the first ranked item.
    :param combo: String for the aggregation metric used in calculating the meta metric.
    :return: AWRF value, Dictionary of group average attention scores (groups are keys).
    """

    unique_grps, grp_count_items = np.unique(
        list(item_group_dict.values()), return_counts=True
    )
    num_unique_rankings = len(ranking_df.columns)
    grp_attention = np.zeros_like(unique_grps, dtype=np.float64)

    for r in range(0, num_unique_rankings):
        single_ranking = ranking_df[ranking_df.columns[r]]  # isolate ranking
        single_ranking = np.array(
            single_ranking[~pd.isnull(single_ranking)]
        )  # drop any NaNs
        num_items = len(single_ranking)
        attn_vals = attention_vector(num_items, p)
        for i in range(0, len(single_ranking)):
            item = single_ranking[i]
            grp_of_item = item_group_dict[item]
            attn_of_item = attn_vals[i]
            # update total group attention
            grp_attention[np.argwhere(unique_grps == grp_of_item)[0,0]] += attn_of_item

    vals = grp_attention / grp_count_items

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


def attention_vector(num_items, p):
    """
    Determine the attention value associate with each position.
    :param num_items: Int, number of items being ranked.
    :param p: Float, proportion of attention provided to the first ranked item.
    :return: Numpy array of attention values
    """
    return np.array([100 * ((1 - p) ** (k - 1)) * p for k in range(1, num_items + 1)])
