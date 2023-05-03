# imports
import numpy as np
import FairRankTune as rt
import pandas as pd
import random
# Experiment on different distributions, across same number of items over 200 trials

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
item_counts = []
distribution = []
g_props = []
phis = []
ndkls = []
ers = []
eeds = []
arps = []
awrfs = []
trial = []
test_num = []
test_n = 1

for num_items in items:
    p = 1/num_items
    for d in range(0, 9):
        group_proportions = distributions[d]
        dist_name = distribution_strings[d]
        r_seed = 10
        print("Group distribution....working on...", dist_name)
        for phi in [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]:
            print("Phi....working on...", phi)
            for trials in range(0,200):
                # For reproducibility
                random.seed(r_seed)
                np.random.seed(r_seed)
                ranking, ranking_ids = rt.GenFromGroups(group_proportions, num_items, phi, 1)
                expdp, avg_exps = rt.EXP(ranking, ranking_ids, 'MinMaxRatio')
                ndkl = rt.NDKL(ranking, ranking_ids)
                eed, avg_exps = rt.EXP(ranking, ranking_ids, 'LTwo')
                arp, _ = rt.ARP(ranking, ranking_ids, 'MaxMinDiff')
                awrf, avg_attns = rt.AWRF(ranking, ranking_ids, p, 'MinMaxRatio')
                item_counts.append(num_items)
                distribution.append(dist_name)
                g_props.append(group_proportions)
                phis.append(phi)
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
                        'phis': phis,
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
                results.to_csv("all_distribution_results.csv", index=False)
                r_seed += 1
