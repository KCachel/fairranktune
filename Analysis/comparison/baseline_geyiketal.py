import FairRankTune as rt
import numpy as np
import pandas as pd
import random

#Experiment to study DetConSort as a data generator
#References: Geyik et al.




distributions = [[.2, .3, .5],
                 [.1, .3, .6],
                 [.2, .3, .32, .05, .13],
                 [.2, .2, .2, .2, .2],
                 [.1, .1, .1, .1, .1, .1, .1, .1, .1, .05, .05],
                 [.3, .08, .3, .17, .1, .05],
                 [.3, .7],
                 [.5, .5],
                 [.1, .9]]

#unfair target distributions for detconsort
dcs_distributions = [[.9, .05, .05],
                 [.9, .05, .05],
                 [.025, .025, .025, .9, .025],
                 [.025, .025, .025, .025, .9],
                 [.01, .01, .01, .01, .01, .01, .01, .01, .01, .01, .9],
                 [.02, .02, .9, .02, .02, .02],
                 [.9, .1],
                 [.9, .1],
                 [.9, .1]]


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
        # For reproducibility
        random.seed(r_seed)
        np.random.seed(r_seed)
        _ranking = np.arange(0, num_items, 1)
        group_ids = np.empty(0, dtype=int)
        for g in range(0, len(group_proportions)):
            group_ids = np.hstack((group_ids, np.tile(int(g), int(num_items * group_proportions[g]))))
        # DetConSort inputs
        k = 1000
        current_ranking_scores = np.random.rand(k)
        for trials in range(0, 200):
            dist_ = dcs_distributions[d] #use unfair target distribution
            reranking, reranking_ids, reranking_scores = rt.DETCONSTSORT(_ranking, group_ids, current_ranking_scores, dist_, k)
            #reranking_ids = [group_ids[item] for item in reranking]
            expdp, avg_exps = rt.EXP(reranking, reranking_ids, 'MinMaxRatio')
            ndkl = rt.NDKL(reranking, reranking_ids)
            eed, avg_exps = rt.EXP(reranking, reranking_ids, 'LTwo')
            arp, _ = rt.ARP(reranking, reranking_ids, 'MaxAbsDiff')
            awrf, avg_attns = rt.AWRF(reranking, reranking_ids, p, 'MinMaxRatio')
            item_counts.append(num_items)
            distribution.append(dist_name)
            g_props.append(group_proportions)
            ers.append(expdp)
            ndkls.append(ndkl)
            eeds.append(eed)
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
            results.to_csv("results_geyiketal.csv", index=False)
            r_seed += 1
