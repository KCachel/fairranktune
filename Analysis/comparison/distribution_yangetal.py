import random
import numpy as np
import pandas as pd
import metrics_utils as met
import random
#Experiment to perform Yang et al. Random Unfair Ranking Generator on binary distributions
# source: https://github.com/DataResponsibly/FairRank/blob/master/dataGenerator.py

def generateUnfairRanking(_ranking, _protected_group, _fairness_probability, group_ids):
    """
        An algorithm for generating rankings with varying degree of fairness.
        :param _ranking: A ranking
        :param _protected_group: The protected group
        :param _fairness_probability: The unfair degree, where 0 is most unfair (unprotected
                       group ranked first) and 1 is fair (groups are mixed randomly
                       in the output ranking)
        :return: returns a ranking that has the specified degree of unfairness w.r.t.
                 the protected group
    """
    # error handling for ranking and protected group
    completeCheckRankingProperties(_ranking, _protected_group)

    if not isinstance(_fairness_probability, (int, float, complex)):
        raise TypeError("Input fairness probability must be a number")
    # error handling for value
    if _fairness_probability > 1 or _fairness_probability < 0:
        raise ValueError("Input fairness probability must be a number in [0,1]")

    pro_ranking = [x for x in _ranking if x not in _protected_group]  # partial ranking of protected member
    unpro_ranking = [x for x in _ranking if x in _protected_group]  # partial ranking of unprotected member
    pro_ranking.reverse()  # prepare for pop function to get the first element
    unpro_ranking.reverse()
    unfair_ranking = []

    while (len(unpro_ranking) > 0 and len(pro_ranking) > 0):
        random_seed = random.random()  # generate a random value in range [0,1]
        if random_seed < _fairness_probability:
            unfair_ranking.append(unpro_ranking.pop())  # insert protected group first
        else:
            unfair_ranking.append(pro_ranking.pop())  # insert unprotected group first

    if len(unpro_ranking) > 0:  # insert the remain unprotected member
        unpro_ranking.reverse()
        unfair_ranking = unfair_ranking + unpro_ranking
    if len(pro_ranking) > 0:  # insert the remain protected member
        pro_ranking.reverse()
        unfair_ranking = unfair_ranking + pro_ranking

    if len(unfair_ranking) < len(_ranking):  # check error for insertation
        print("Error!")

    item_numpy = np.asarray(_ranking)
    ranking_group_ids = [group_ids[np.argwhere(item_numpy == i)[0][0]] for i in unfair_ranking]
    return unfair_ranking, ranking_group_ids


# Function for error handling
def completeCheckRankingProperties(_ranking, _protected_group):
    """
        Check whether input ranking and protected group is valid.
        :param _ranking: A ranking
        :param _protected_group: The protected group

        :return: no returns. Raise errors if founded.
    """
    # error handling for input type
    #    if not isinstance(_ranking, (list, tuple, np.ndarray)) and not isinstance( _ranking, basestring ):
    #        raise TypeError("Input ranking must be a list-wise structure defined by '[]' symbol")
    #    if not isinstance(_protected_group, (list, tuple, np.ndarray)) and not isinstance( _protected_group, basestring ):
    #        raise TypeError("Input protected group must be a list-wise structure defined by '[]' symbol")

    user_N = len(_ranking)
    pro_N = len(_protected_group)

    # error handling for input value
    if user_N <= 0:  # check size of input ranking
        raise ValueError("Please input a valid ranking")
    if pro_N <= 0:  # check size of input ranking
        raise ValueError("Please input a valid protected group whose length is larger than 0")

    if pro_N >= user_N:  # check size of protected group
        raise ValueError("Please input a protected group with size less than total user")

    if len(set(_ranking)) != user_N:  # check for repetition in input ranking
        raise ValueError("Please input a valid complete ranking")

    if len(set(_protected_group)) != pro_N:  # check repetition of protected group
        raise ValueError("Please input a valid protected group that have no repetitive members")

    if len(set(_protected_group).intersection(_ranking)) <= 0:  # check valid of protected group
        raise ValueError("Please input a valid protected group that is a subset of total user")

    if len(set(_protected_group).intersection(_ranking)) != pro_N:  # check valid of protected group
        raise ValueError("Please input a valid protected group that is a subset of total user")


distributions = [[.3, .7],
                 [.5, .5],
                 [.1, .9]]

items = [1000]

distribution_strings = ['Dist g',
                        'Dist h',
                        'Dist i']
item_counts = []
distribution = []
g_props = []
fps = []
ndkls = []
ers = []
eeds = []
arps = []
awrfs = []
trial = []
test_num = []
test_n = 1

for num_items in items:
    p = 1 / num_items
    for d in range(0, 3):
        group_proportions = distributions[d]
        dist_name = distribution_strings[d]
        r_seed = 10
        print("Group distribution....working on...", dist_name)
        for fp in [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]:
            print("fp....working on...", fp)
            for trials in range(0, 200):
                # For reproducibility
                random.seed(r_seed)
                np.random.seed(r_seed)
                _ranking = np.arange(0,num_items,1)
                _protected_group = np.arange(0, int(group_proportions[0]*num_items),1)
                group_ids = np.empty(0, dtype=int)
                for g in range(0, len(group_proportions)):
                    group_ids = np.hstack((group_ids, np.tile(int(g), int(num_items * group_proportions[g]))))
                ranking, ranking_ids = generateUnfairRanking(_ranking, _protected_group, fp, group_ids)
                expdp, avg_exps = met.calculate_er_singh(np.asarray(ranking), np.asarray(ranking_ids))
                ndkl = met.calculate_ndkl_geyik(np.asarray(ranking), np.asarray(ranking_ids))
                eel, avg_exps = met.calculate_eed_diaz(np.asarray(ranking), np.asarray(ranking_ids))
                arp = met.rank_parity_score(met.fpr(np.asarray(ranking), np.asarray(ranking_ids)))
                awrf, avg_attns = met.calculate_awrf_sapiezynski(np.asarray(ranking), np.asarray(ranking_ids), p)
                item_counts.append(num_items)
                distribution.append(dist_name)
                g_props.append(group_proportions)
                fps.append(fp)
                ers.append(expdp)
                ndkls.append(ndkl)
                eeds.append(eel)
                arps.append(arp)
                awrfs.append(awrf)
                trial.append(trials)
                test_num.append(test_n)
                test_n += 1

                # save results
                data = {'item_counts': item_counts,
                        'distribution': distribution,
                        'g_props': g_props,
                        'phis': fps,
                        'ndkls': ndkls,
                        'ers': ers,
                        'eeds': eeds,
                        'arps': arps,
                        'awrfs': awrfs,
                        'trials': trial,
                        'test_num': test_num
                        }

                results = pd.DataFrame(data)
                print(results)
                #results.to_csv("distribution_robustness_results_yangetal.csv", index=False)
                r_seed += 1
