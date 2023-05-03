import numpy as np
import random

import FairRankTune.RankTune
from FairRankTune import *


# ADJUST BELOW VARIABLES AS DESIRED
group_proportions = [.2, .3, .5]
num_items = 1000

#FOR REPRODUCABILITY
r_seed = 10
random.seed(r_seed)
np.random.seed(r_seed)


# FOR GENERATING AND PLOTTING
phi_plot = []
ndkl_plot = []
er_plot = []
eed_plot = []
arp_plot = []
awrf_plot = []

for phi in [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]:

    num_items = 1000 #number of items to be ranked
    group_proportions = np.asarray([0.2, .3, .5]) #each group's size as % of num_items
    phi = 0.8 # unfairness tuning parameter
    r_cnt = 1 #generate only 1 ranking
    ranking, ranking_ids = FairRankTune.RankTune.GenFromGroups(np.asarray([0.2, .3, .5]), #group proportions
                                                               1000, #number of items
                                                               0.9, #unfairness tuning parameter
                                                               1) #how many ranking to generate

    ranking, ranking_ids = FairRankTune.RankTune.GenFromGroups(np.asarray([0.2, .3, .5]), #group proportions
                                                               1000, #number of items
                                                               0.9, #unfairness tuning parameter
                                                               1) #how many ranking to generate
    #Use generated ranking to calculate exposure two different ways
    val, per_group_exp = FairRankTune.Metrics.EXP(ranking, #ranking of items to assess
        ranking_ids, #group membership of items
        "MinMaxRatio") #formula for combining per-group metrics
    val, per_group_exp = FairRankTune.Metrics.EXP(ranking, #ranking of items to assess
        ranking_ids, #group membership of items
        "LTwo") #formula for combining per-group metrics


    arp_val = FairRankTune.Metrics.ARP(ranking, #he
                                    ranking_ids, #comment
                                    'MaxMinRatio')
