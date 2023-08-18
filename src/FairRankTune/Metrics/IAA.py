import pandas as pd
from FairRankTune.Metrics.ComboUtil import *

# Script to calculate Inequity of Amortized Attention Fair Ranking Metric.
# References: Biega, A.J., Gummadi, K.P., & Weikum, G. (2018). Equity of Attention: Amortizing Individual Fairness in Rankings.
# The 41st International ACM SIGIR Conference on Research & Development in Information Retrieval.


def IAA(ranking_df, relevance_df):
    """
    Calculate Inequity of Amortized Attention (Biega et al.).
    :param ranking_df: Pandas dataframe of ranking(s).
    :param relevance_df: Pandas dataframe of relevance scores associated with each item in ranking(s).
    :return: IAA value
    """

    num_unique_rankings = len(ranking_df.columns)
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
            assert "IAA requires that relevance score be between 0 and 1."
        attention = __attention_at_position_array(len(single_ranking))

        attention_vals = []
        relevance_vals = []
        for i in range(0, len(single_ranking)):
            attention_vals.append(attention[i])
            relevance_vals.append(assoc_rel[i])

        IAA = np.abs(
            np.asarray(attention_vals) - np.asarray(relevance_vals)
        ).sum()  # Eq. 1 in Biega et al.
        return IAA


def __attention_at_position_array(num_items):
    """
    Calculate the attention associated with each position in the ranking.
    :param num_items: Int, number of items to be ranked.
    :return: Numpy array of attention scores.
    """
    return np.array([(1 / (np.log2(i + 1))) for i in range(1, num_items + 1)])
