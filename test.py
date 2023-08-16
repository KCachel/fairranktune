import numpy as np
import pandas as pd

import FairRankTune
import FairRankTune as frt
import random



ranking_df, item_group_dict = frt.RankTune.GenFromGroups(np.asarray([.1, .9]), 1000, 0, 1)
print(frt.Metrics.EXP(ranking_df, item_group_dict, 'MinMaxRatio'))


ranking_df = pd.read_csv('testdata.csv')

item_group_dict = {
        "a": 0,
        "b": 0,
        "e": 0,
        "f": 0,
        "g": 0,
        "c": 1,
        "d": 1,
    }


# #frt.Metrics.EXP(ranking_df, item_group_dict, 'MinMaxRatio')
# print(frt.Metrics.ARP(ranking_df, item_group_dict, 'MaxAbsDiff'))
# print(frt.Metrics.EXPRU(ranking_df, item_group_dict, pd.DataFrame(np.ones_like(ranking_df)*4), pd.DataFrame(np.ones_like(ranking_df)*-2), 'MaxAbsDiff'))
# #print(frt.Metrics.NDKL(ranking_df, item_group_dict))

#FOR REPRODUCABILITY
r_seed = 10
random.seed(r_seed)
np.random.seed(r_seed)

#generate unfair ranking
phi = 0
group_proportions = np.asarray([.2, .6, .1, .1])
num_items = 1000
score_dist = 'uniform' #give items scores from a uniform distribution
r_cnt = 1
ranking, group_dict, scores = frt.ScoredGenFromGroups(group_proportions, num_items, phi, r_cnt, score_dist)
groups = np.asarray([group_dict[i] for i in ranking[0].to_numpy()])
# group_dict = {}
# for r in range(0, len(ranking)):
#         group_dict[(ranking[r])] = groups[r]
#measure bias
arpOLD, _ = frt.ARP(ranking, group_dict, 'MaxMinDiff')
awrfOLD, avg_attns = frt.AWRF(ranking, group_dict, 1/1000, 'MinMaxRatio')
ndklOLD = frt.NDKL(ranking, group_dict)
eedOLD, avg_exps1 = frt.EXP(ranking, group_dict, 'LTwo')
expOLD, avg_exps2 = frt.EXP(ranking, group_dict, 'MinMaxRatio')
erbeOLD, avg_exps3 = frt.ERBE(ranking, group_dict, .1, 'MinMaxRatio')
erbpOLD, avg_exps4 = frt.ERBP(ranking, group_dict, .1, 'MinMaxRatio')
iaaOLD = frt.IAA(ranking, pd.DataFrame(scores))
expuOLD, _ = FairRankTune.EXPU(ranking,group_dict, pd.DataFrame(scores), 'MinMaxRatio')
print("ER fairness prior to reranking: ", expOLD)
print("NDKL fairness prior to reranking: ", ndklOLD)
print("EED fairness prior to reranking: ", eedOLD)
print("ARP fairness prior to reranking: ", arpOLD)
print("AWRF fairness prior to reranking: ", awrfOLD)
print("ERBE fairness prior to reranking: ", erbeOLD)
print("ERBP fairness prior to reranking: ", erbpOLD)
print("IAA individual fairness prior to reranking: ", iaaOLD)
print("EXPU fairness prior to reranking: ", expuOLD)

#rerank to be fair
distribution = np.asarray([.2, .6, .1, .1])
reranking, reranking_ids, reranking_scores = frt.DETCONSTSORT(ranking, group_dict, scores, distribution, 800)

#measure bias again
arpPOST, _ = frt.ARP(reranking, reranking_ids, 'MaxMinDiff')
awrfPOST, avg_attns = frt.AWRF(reranking, reranking_ids, 1/1000, 'MinMaxRatio')
ndklPOST = frt.NDKL(reranking, reranking_ids)
eedPOST, avg_exps = frt.EXP(reranking, reranking_ids, 'LTwo')
expPOST, avg_exps = frt.EXP(reranking, reranking_ids, 'MinMaxRatio')
erbePOST, avg_exps = frt.ERBE(reranking, reranking_ids, .1, 'MinMaxRatio')
erbpPOST, avg_exps = frt.ERBP(reranking, reranking_ids, .1, 'MinMaxRatio')
iaaPOST = frt.IAA(reranking, reranking_scores)
expuPOST, _ = FairRankTune.EXPU(reranking,reranking_ids, reranking_scores, 'MinMaxRatio')
print("ARP fairness after reranking: ", arpPOST)
print("AWRF fairness after reranking: ", awrfPOST)
print("NDKL fairness after reranking: ", ndklPOST)
print("EED fairness after reranking: ", eedPOST)
print("ER fairness after reranking: ", expPOST)
print("ERBE fairness after reranking: ", erbePOST)
print("ERBP fairness after reranking: ", erbpPOST)
print("IAA fairness after reranking: ", iaaPOST)
print("EXPU fairness after reranking: ", expuPOST)