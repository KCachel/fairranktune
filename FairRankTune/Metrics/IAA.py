import numpy as np
from FairRankTune.Metrics.ComboUtil import *
# Script to calculate Inequity of Amortized Attention Fair Ranking Metric.
# References: Biega, A.J., Gummadi, K.P., & Weikum, G. (2018). Equity of Attention: Amortizing Individual Fairness in Rankings.
# The 41st International ACM SIGIR Conference on Research & Development in Information Retrieval.
def IAA(ranking, relevance):
    """
    Calculate IAA score (Biega et. al)
    :param ranking: Numpy array of ranking methods
    :param relevance: Numpy array of relevance scores
    :return: IAA value, numpy array of group average exposure
    """

    #check relevance is between 0 and 1
    if np.any((relevance < 0) | (relevance > 1)):
        assert("IAA requires that relevance score be between 0 and 1. ")

    num_items = len(ranking)
    attention = attention_at_position_array(num_items)
    IAA = 0
    for i in range(0, num_items):
        att_of_item = attention[i]
        rel_of_item = relevance[i]
        IAA += np.abs(att_of_item - rel_of_item)

    return IAA


def attention_at_position_array(num_items):
    return np.array([(1 / (np.log2(i + 1))) for i in range(1, num_items + 1)])