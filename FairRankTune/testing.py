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
    ranking, ranking_ids = FairRankTune.RankTune.GenFromGroups(group_proportions, num_items, phi, 1)
    arp_val = FairRankTune.Metrics.ARP(ranking, ranking_ids, 'MaxMinRatio')