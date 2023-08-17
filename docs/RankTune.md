# RankTune

## Overview

## Usage

### Using Group Sizes

### Using an Existing Dataset

### Generating Scores With the Ranking



## How does it work?

RankTune is a fairness-tunable  ranked data generation method. It constructs a ranking(s) ```ranking_df``` by placing items into the constructed ranking from top to bottom. The idea behind RankTune is that to construct a "fair" ranking, each time we place an item in the generated ranking, the likelihood of placing an item in a given group should be equal to that group's proportion of the total items (i.e., if a group is 20% of the item pool, then it should have a 20% chance of being placed). Then, on the other side of the spectrum, if we want a completely "unfair" ranking, we should place items into the rankings such that groups are ordered by increasing size from small to large. In this way, smaller groups  get bigger proportions of favorable positions, which violates statistical parity fairness. 

To generate rankings along the statistical parity fairness spectrum, RankTune samples a random number in the [0, 1] interval each time it places an item. We design this interval to have "regions" that map to groups. In this way, the unfairness tuning parameter ```phi``` controls representativeness, i.e.,  how fairly each group is represented in the ranking. Specifically, when ```phi = 1``` , then  each group is fairly represented. Thus each group's region is equal to the group's proportion of the pool (fair). As ```phi``` decreases, the fair representation of each group degrades because regions are distorted in such a way that smaller groups have larger regions compared to their proportion of the total pool (unfair). The fairness tuning parameter ```phi``` is used to create the regions prior to placing any items into the generated ranking.