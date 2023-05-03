# imports
import numpy as np
import FAIRRANKTUNE as rt
import pandas as pd
import random
import time
#Experiment for timing FairRankTune. Helper function to check inputs were uncommented during timining.
# For reproducibility
random.seed(10)
np.random.seed(10)

distributions = [[.2, .3, .5],
                 [.1, .3, .6],
                 [.2, .3, .1, .05, .03],
                 [.2, .2, .2, .2, .2],
                 [.1, .1, .1, .1, .1, .1, .1, .1, .1, .05, .05],
                 [.6, .08, .02, .15, .1, .05],
                 [.3, .7],
                 [.5, .5],
                 [.1, .9]]

items = [100, 1000, 10000, 100000, 500000]


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
avg_time = []


for num_items in items:
    p = 1 / 100
    for d in range(0, 9):
        group_proportions = distributions[d]
        dist_name = distribution_strings[d]
        times = []
        for phi in [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]:
            start_time = time.time()
            ranking, ranking_ids = rt.GenFromGroups(group_proportions, num_items, phi, 1)
            end_time = time.time()
            times.append(end_time - start_time)


        item_counts.append(num_items)
        distribution.append(dist_name)
        avg_time.append(np.mean(times))
        # save results
        data = {'item_counts': item_counts,
                'distribution': distribution,
                'avg_time': avg_time
                }

        results = pd.DataFrame(data)
        print(results)
        results.to_csv("timing_results.csv", index=False)



