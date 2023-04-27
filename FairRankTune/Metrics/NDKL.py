import numpy as np
# Script to calculate NDKL metric
# References: Geyik, S. C., Ambler, S., & Kenthapadi, K. (2019, July).
# Fairness-aware ranking in search & recommendation systems with application to linkedin talent search.
# In Proceedings of the 25th acm sigkdd international conference on knowledge discovery & data mining (pp. 2221-2231).

def kl_divergence(p, q):
    """ Epsilon is used here to avoid P or Q is equal to 0. """
    epsilon = 0.0000001
    p = p + epsilon
    q = q + epsilon

    return np.sum(p * np.log(p / q))


def NDKL(ranking, group_ids):
    """
    Calculate NDKL (Geyik et al)
    :param ranking:
    :param group_ids:
    :return:
    """
    # Stores the number of groups and the length of the list
    num_groups, list_length = np.max(group_ids), len(group_ids)

    # Stores the distributions of the groups based on the full list
    dr = distributions(group_ids, num_groups)

    # Define Z as an array of Z scores, which is the exposure function
    Z = Z_Vector(list_length)

    # Return the results fo 1 over the sum of Z scores times the kl_divergences of the sublists multiplied by their respective Z score
    return (1 / np.sum(Z)) * np.sum(
        [Z[i] * kl_divergence(distributions(group_ids[0: i + 1], num_groups), dr) for i in range(0, list_length)])

def distributions(passed_ranked_list: np.array, num_groups: int) -> np.array:
    # Returns an array with each group id's probability based on the passed ranked_list
    return np.array([prob(i, passed_ranked_list) for i in range(0, num_groups + 1)])
def prob(a, b):
    return ((b == a).sum()) / len(b)

def Z_Vector(k):
    return 1 / np.log2(np.array(range(0, k)) + 2)