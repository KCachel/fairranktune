import numpy as np
import FairRankTune as rt
import pandas as pd

import random
#Experiment to construct partially synthetic data from lsac dataset
output = 'law_synthetic_generation.csv'

law_raw = pd.read_csv('law_data.csv', sep=',')
item_ids = np.arange(0, 21791, 1, dtype=int)

#Score to induce a ranking
sex = np.array(law_raw["sex"])
sex = sex - 1 #zero index
score = np.array(law_raw["LSAT"])

#sort items by score for initial ranking
zipped = zip(score, item_ids)
sorted_zipped = sorted(zipped)
init_ranking = np.asarray([element for _, element in sorted_zipped])
init_group_ids = np.asarray([sex[np.argwhere(item_ids == i)[0][0]]  for i in init_ranking])


item_counts = []
phis = []
ndkls = []
ers = []
eeds = []
arps = []
awrfs = []
trial = []
test_num = []
test_n = 1

p = 1/len(init_ranking)
expdp, avg_exps = rt.EXP(init_ranking, init_group_ids, 'MinMaxRatio')
ndkl = rt.NDKL(init_ranking, init_group_ids)
eed, avg_exps = rt.EXP(init_ranking, init_group_ids, 'LTwo')
arp, _ = rt.ARP(init_ranking, init_group_ids, 'MaxMinDiff')
awrf, avg_attns = rt.AWRF(init_ranking, init_group_ids, p, 'MinMaxRatio')
phis.append("original")
ers.append(expdp)
ndkls.append(ndkl)
eeds.append(eed)
arps.append(arp)
awrfs.append(awrf)
trial.append(0)
test_num.append(test_n)
test_n += 1

# save results
data = {'phis': phis,
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
results.to_csv(output, index=False)



# For reproducibility
r_seed = 10


for phi in [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]:
    print("Phi....working on...", phi)
    for trials in range(0, 10):
        # For reproducibility
        random.seed(r_seed)
        np.random.seed(r_seed)
        ranking, ranking_ids = rt.GenFromItems(item_ids, sex,phi, 1)
        expdp, avg_exps = rt.EXP(ranking, ranking_ids, 'MinMaxRatio')
        ndkl = rt.NDKL(ranking, ranking_ids)
        eed, avg_exps = rt.EXP(ranking, ranking_ids, 'LTwo')
        arp, _ = rt.ARP(ranking, ranking_ids, 'MaxMinDiff')
        awrf, avg_attns = rt.AWRF(ranking, ranking_ids, p, 'MinMaxRatio')
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
        data = {'phis': phis,
                'ndkls': ndkls,
                'ers': ers,
                'eeds': eeds,
                'arps': arps,
                'awrfs': awrfs,
                'trials': trial,
                'test_num': test_num
                }

        results = pd.DataFrame(data)
        # print(results)
        results.to_csv(output, index=False)
        r_seed += 1

