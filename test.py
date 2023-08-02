import numpy as np
import pandas as pd
import FairRankTune as frt
import random


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


#frt.Metrics.EXP(ranking_df, item_group_dict, 'MinMaxRatio')
frt.Metrics.ARP(ranking_df, item_group_dict, 'MaxAbsDiff')

#FOR REPRODUCABILITY
r_seed = 10
random.seed(r_seed)
np.random.seed(r_seed)


