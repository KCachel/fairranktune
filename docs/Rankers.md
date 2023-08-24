# Rankers

## Fair Ranking Algorithms
```FairRankTune``` provides [fair ranking algorithms](#supported-fair-ranking-algorithms) in the ```Rankers``` module. These fair ranking algorithms can be used to re-rank a given ranking with the objective of making the resulting ranking fair. 


## Supported Fair Ranking Algorithms

### Epsilon-Greedy Re-Ranker
Epsilon-Greedy takes as input a ranking and repeatedly swaps pairs of items so that each item has probability $\epsilon$ (```epsilon```) of swapping with a random item below it. It does not require a specific notion of fairness or prior knowledge of group distributions. It does use random swapping, thus it is recommended to set a random seed for reproducibility. To learn more see [Feng et al.](https://doi.org/10.1609/aaai.v36i11.21445) where it was introduced to improve group fairness.

Usage:
```python
import FairRankTune as frt
import numpy as np
import pandas as pd
from FairRankTune import RankTune, Metrics
import random

#Generate a biased (phi = 0) ranking of 1000 items, with two groups of 100 and 900 items each.
group_proportions = np.asarray([.1, .9]) #Array of group proportions
num_items = 1000 #1000 items to be in the generated ranking
phi = 0 #Biased ranking
r_cnt = 1 #Generate 1 ranking
ranking_df, item_group_dict, scores_df = frt.RankTune.ScoredGenFromGroups(group_proportions,  num_items, phi, r_cnt, 'uniform', seed)

#Calculate EXP with a MinMaxRatio
EXP_minmax, avg_exposures_minmax = frt.Metrics.EXP(ranking_df, item_group_dict, 'MinMaxRatio')
print("EXP before Epsilon-Greedy: ", EXP_minmax, "avg_exposures before Epsilon-Greedy: ", avg_exposures_minmax)


#Rerank using Epsilon-Greedy
seed = 2 #For reproducibility
epsilon = .6 
reranking_df, item_group_d, reranking_scores = frt.Rankers.EPSILONGREEDY(ranking_df, item_group_dict, scores_df, epsilon, seed)

#Calculate EXP with a MinMaxRatio post Epsilon-Greedy
EXP, avg_exposures= frt.Metrics.EXP(reranking_df, item_group_d, 'MinMaxRatio')
print("EXP after Epsilon-Greedy: ", EXP, "avg_exposures after Epsilon-Greedy: ", avg_exposures)
```

Output:
```python
EXP before Epsilon-Greedy:  0.5420744267551784 avg_exposures before Epsilon-Greedy:  {0: 0.2093867087428094, 1: 0.11350318011191189}
EXP after Epsilon-Greedy:  0.7689042373241246 avg_exposures after Epsilon-Greedy:  {0: 0.15541589156986096, 1: 0.1194999375755728}
```
```epsilon``` must be between $[0,1]$ and a ```seed``` is passed for reproducibility.

Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@article{Feng_Shah_2022, title={Has CEO Gender Bias Really Been Fixed? Adversarial Attacking and Improving Gender Fairness in Image Search},
volume={36},
url={https://ojs.aaai.org/index.php/AAAI/article/view/21445},
DOI={10.1609/aaai.v36i11.21445},
number={11},
journal={Proceedings of the AAAI Conference on Artificial Intelligence},
author={Feng, Yunhe and Shah, Chirag},
year={2022},
month={Jun.},
 pages={11882-11890} }
```
</details>

### DetConstSort Re-Ranker
DetConstSort takes as input a given ranking, and re-ranks items in it to create a top-k fair ranking. Fairness is achieved by setting the ```distribution``` dictionary.  In ```distribution``` the keys are group identifiers and the value is the desired group proportion. For any particular position k and for any group ```g```, DetConstSort ensures that group occurs $\lfloor$ ```distribution[g]``` $*k \rfloor$ in the resulting ranking. DetConstSort algorithm also tries improve the utility of the ranking by ensuring that items with better scores are placed higher in the ranking so long as the ranking satisfies the feasibility criteria. To learn more see [Geyik et al.](https://dl.acm.org/doi/10.1145/3292500.3330691).


Usage:
```python
import FairRankTune as frt
import numpy as np
import pandas as pd
from FairRankTune import RankTune, Metrics
import random
random.seed(10)

#Generate a biased (phi = 0) ranking of 1000 items, with two groups of 100 and 900 items each.
seed = 2
ranking_df, item_group_dict, scores_df = frt.RankTune.ScoredGenFromGroups(np.asarray([.1, .9]),  1000, 0, 1, 'uniform', seed)

#Calculate EXP with a MinMaxRatio
EXP_minmax, avg_exposures_minmax = frt.Metrics.EXP(ranking_df, item_group_dict, 'MinMaxRatio')
print("EXP before DetConstSort: ", EXP_minmax, "avg_exposures before DetConstSort: ", avg_exposures_minmax)


#Rerank using DetConstSort
distribution = dict(zip([0, 1], [.1, .9])) #set distribution for statistical parity
k = 800 #only ranking 800 items of the provided 1000 
reranking_df, item_group_d, reranking_scores = frt.Rankers.DETCONSTSORT(ranking_df, item_group_dict, scores_df, distribution, k)

#Calculate EXP with a MinMaxRatio post DetConstSort
EXP, avg_exposures= frt.Metrics.EXP(reranking_df, item_group_d, 'MinMaxRatio')
print("EXP after DetConstSort: ", EXP, "avg_exposures after DetConstSort: ", avg_exposures)
```

Output:
```python
EXP before DetConstSort:  0.5420744267551784 avg_exposures before DetConstSort:  {0: 0.2093867087428094, 1: 0.11350318011191189}
EXP after DetConstSort:  0.9738302276209081 avg_exposures after DetConstSort:  {0: 0.12535449974404395, 1: 0.12872315542133886}
```

Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@article{Feng_Shah_2022, title={Has CEO Gender Bias Really Been Fixed? Adversarial Attacking and Improving Gender Fairness in Image Search},
volume={36},
url={https://ojs.aaai.org/index.php/AAAI/article/view/21445},
DOI={10.1609/aaai.v36i11.21445},
number={11},
journal={Proceedings of the AAAI Conference on Artificial Intelligence},
author={Feng, Yunhe and Shah, Chirag},
year={2022},
month={Jun.},
 pages={11882-11890} }
```
</details>



## Contributing Fair Ranking Algorithms
We believe in open-source community driven software. Please [reach out](mailto:kathleen.cachel@gmail.com?subject=[GitHub]%20fairranktune) to expand the ```FairRankTune``` algorithm offerings. 