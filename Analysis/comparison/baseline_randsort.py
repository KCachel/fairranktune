import numpy as np
import pandas as pd
import metrics_utils as met
import random

#Experiment to study RandSort as a data generator



def randsort_normal(current_ranking, ranking_grp_ids):
    scores = np.random.standard_normal(size = len(current_ranking))
    sorted_scores, sorted_items = zip(*sorted(zip(scores, current_ranking), reverse = True))
    sorted_grp_ids = [ranking_grp_ids[item] for item in sorted_items]
    return sorted_items, sorted_grp_ids

def randsort_uniform(current_ranking, ranking_grp_ids):
    scores = np.random.uniform(0, 1, size=len(current_ranking))
    sorted_scores, sorted_items = zip(*sorted(zip(scores, current_ranking), reverse=True))
    sorted_grp_ids = [ranking_grp_ids[item] for item in sorted_items]
    return sorted_items, sorted_grp_ids

distributions = [[.2, .3, .5],
                 [.1, .3, .6],
                 [.2, .3, .32, .05, .13],
                 [.2, .2, .2, .2, .2],
                 [.1, .1, .1, .1, .1, .1, .1, .1, .1, .05, .05],
                 [.3, .08, .3, .17, .1, .05],
                 [.3, .7],
                 [.5, .5],
                 [.1, .9]]


items = [1000]


distribution_strings = ['Dist a',
                        'Dist b',
                        'Dist c',
                        'Dist d',
                        'Dist e',
                        'Dist f',
                        'Dist g',
                        'Dist h',
                        'Dist i']
####### RANDSORT WITH NORMAL
item_counts = []
distribution = []
g_props = []
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
    for d in range(0, 9):
        group_proportions = distributions[d]
        dist_name = distribution_strings[d]
        r_seed = 10
        print("Group distribution....working on...", dist_name)
        for trials in range(0, 200):
            # For reproducibility
            random.seed(r_seed)
            np.random.seed(r_seed)
            _ranking = np.arange(0,num_items,1)
            group_ids = np.empty(0, dtype=int)
            for g in range(0, len(group_proportions)):
                group_ids = np.hstack((group_ids, np.tile(int(g), int(num_items * group_proportions[g]))))
            reranking, reranking_ids = randsort_normal(_ranking, group_ids)
            expdp, avg_exps = met.calculate_er_singh(np.asarray(reranking), np.asarray(reranking_ids))
            ndkl = met.calculate_ndkl_geyik(np.asarray(reranking), np.asarray(reranking_ids))
            eel, avg_exps = met.calculate_eed_diaz(np.asarray(reranking), np.asarray(reranking_ids))
            arp = met.rank_parity_score(met.fpr(np.asarray(reranking), np.asarray(reranking_ids)))
            awrf, avg_attns = met.calculate_awrf_sapiezynski(np.asarray(reranking), np.asarray(reranking_ids), p)
            item_counts.append(num_items)
            distribution.append(dist_name)
            g_props.append(group_proportions)
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
                    'ndkls': ndkls,
                    'ers': ers,
                    'eeds': eeds,
                    'arps': arps,
                    'awrfs': awrfs,
                    'trials': trial,
                    'test_num': test_num
                    }

            results = pd.DataFrame(data)
            #print(results)
            results.to_csv("results_randsortnormal.csv", index=False)
            r_seed += 1

####### RANDSORT WITH UNIFORM
item_counts = []
distribution = []
g_props = []
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
    for d in range(0, 9):
        group_proportions = distributions[d]
        dist_name = distribution_strings[d]
        r_seed = 10
        print("Group distribution....working on...", dist_name)
        for trials in range(0, 200):
            # For reproducibility
            random.seed(r_seed)
            np.random.seed(r_seed)
            _ranking = np.arange(0,num_items,1)
            group_ids = np.empty(0, dtype=int)
            for g in range(0, len(group_proportions)):
                group_ids = np.hstack((group_ids, np.tile(int(g), int(num_items * group_proportions[g]))))
            reranking, reranking_ids = randsort_uniform(_ranking, group_ids)
            expdp, avg_exps = met.calculate_er_singh(np.asarray(reranking), np.asarray(reranking_ids))
            ndkl = met.calculate_ndkl_geyik(np.asarray(reranking), np.asarray(reranking_ids))
            eel, avg_exps = met.calculate_eed_diaz(np.asarray(reranking), np.asarray(reranking_ids))
            arp = met.rank_parity_score(met.fpr(np.asarray(reranking), np.asarray(reranking_ids)))
            awrf, avg_attns = met.calculate_awrf_sapiezynski(np.asarray(reranking), np.asarray(reranking_ids), p)
            item_counts.append(num_items)
            distribution.append(dist_name)
            g_props.append(group_proportions)
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
                    'ndkls': ndkls,
                    'ers': ers,
                    'eeds': eeds,
                    'arps': arps,
                    'awrfs': awrfs,
                    'trials': trial,
                    'test_num': test_num
                    }

            results = pd.DataFrame(data)
            #print(results)
            results.to_csv("results_randsortuniform.csv", index=False)
            r_seed += 1


