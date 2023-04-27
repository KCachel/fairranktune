import numpy as np
# Script to calculate EE-D metric using L2 norm.
# References: Diaz, F., Mitra, B., Ekstrand, M. D., Biega, A. J., & Carterette, B. (2020, October).
# Evaluating stochastic rankings with expected exposure.
# In Proceedings of the 29th ACM international conference on information & knowledge management (pp. 275-284).
# Raj, A., & Ekstrand, M. D. (2022, July). Measuring Fairness in Ranked Results: An Analytical and Empirical Comparison.
# In Proceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval (pp. 726-736).
def calculate_eed_diaz(ranking, group_ids):
    """
        Calculate EED score (Diaz et. al)
        :param ranking: Numpy array of ranking methods
        :param group_ids: Numpy array of group ids
        :return: EED value, numpy array of group average exposure
        """
    unique_grps, grp_count_items = np.unique(group_ids, return_counts=True)
    num_items = len(ranking)
    exp_vals = exp_at_position_array(num_items)
    grp_exposures = np.zeros_like(unique_grps, dtype=np.float64)
    for i in range(0,num_items):
        grp_of_item = group_ids[i]
        exp_of_item = exp_vals[i]
        #update total group exp
        grp_exposures[grp_of_item] += exp_of_item

    avg_exp_grp = grp_exposures / grp_count_items
    result = np.linalg.norm(avg_exp_grp, 2)
    return result, avg_exp_grp

def exp_at_position_array(num_items):
    return np.array([(1/(np.log2(i+1))) for i in range(1,num_items+1)])