# Home

<div align="center">
  <img src="https://raw.githubusercontent.com/KCachel/fairranktune/main/.github/images/FairRankTune.png">
</div>

<p align="center">
  <!-- Python -->
  <a href="https://www.python.org" alt="Python"><img src="https://badges.aleen42.com/src/python.svg"></a>
  <!-- Version -->
  <a href="https://pypi.org/project/FairRankTune/"><img src="https://img.shields.io/pypi/v/FairRankTune?color=light-green" alt="PyPI version"></a>
  <!-- Docs -->
  <a href="https://kcachel.github.io/fairranktune"><img src="https://img.shields.io/badge/docs-passing-<COLOR>.svg" alt="Documentation Status"></a>
  <!-- Black -->
  <a href="https://github.com/psf/black" alt="Code style: black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
  <!-- License -->
  <a href="https://www.tldrlegal.com/license/bsd-3-clause-license-revised"><img src="https://img.shields.io/badge/license-BSD3-blue" alt="License: BSD 3-Clause"></a>
</p>

## 📍 Introduction

[FairRankTune](https://github.com/KCachel/fairranktune) is a  an open-source [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) toolkit supporting end-to-end fair ranking workflows, analysis, auditing, and experimentation. FairRankTune provides researchers, practitioners, and educators with a self-contained module for generating ranked data, ranking strategies, and popular ranking-based fairness metrics.

For a quick overview, follow the [Usage](#💡-usage) section.

For a in-depth overview, follow the [Examples](#📖-examples) section.


## ✨ Features


### 🎨 Fairness-Aware Ranked Data Generation

```RankTune``` is a pseudo-stochastic data generation method for creating fairness-aware ranked lists using the fairness concept of statistical parity. Included in the ```RankTune``` module, it creates ranking(s) based on the ```phi``` representativeness parameter. When ```phi = 0``` then the generated ranked list(s) does not represent groups fairly, and as ```phi``` increases groups are represented more and more fairly; thus ```phi = 1``` groups are fairly represented. RankTune uses a [pseudo-random process](https://kcachel.github.io/fairranktune/RankTune/#how-does-it-work) to generate fairness-aware ranked data. RankTune can generate ranked data from [user provided group sizes](https://kcachel.github.io/fairranktune/RankTune/#using-group-sizes), from [existing datasets](https://kcachel.github.io/fairranktune/RankTune/#using-an-existing-dataset), along with [producing relevance scores](https://kcachel.github.io/fairranktune/RankTune/#generating-scores-with-the-ranking) accompanying the ranked list(s). 


Please refer to the [documentation](https://kcachel.github.io/fairranktune/RankTune/) for additional information. 

### 📏 Metrics

```FairRankTune ``` provides several metrics for evaluating the fairness of ranked lists in the ```Metrics``` module. The table below provides a high-level overview of each metric. These metrics encompass a variety of fair ranking metrics, including both [group](https://en.wikipedia.org/wiki/Fairness_(machine_learning)#Group_Fairness_criteria) and [individual](https://en.wikipedia.org/wiki/Fairness_(machine_learning)#Individual_Fairness_criteria) fairness, along with both score-based and statistical parity metrics. 


| **Metric** | **Abbreviation** | **Fairness (Group or Individual)** | **Score-based** | **Statistical Parity** | **Reference** |
|---|:---:|:---:|:---:|:---:|:---:|
| [Group Exposure](https://kcachel.github.io/fairranktune/Metrics/#group-exposure-exp) | EXP | Group | No | Yes | [Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088) |
| [Exposure Utility](https://kcachel.github.io/fairranktune/Metrics/#exposure-realized-utility-expru) | EXPU | Group | Yes | No | [Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088) |
| [Exposure Realized Utility](https://kcachel.github.io/fairranktune/Metrics/#exposure-realized-utility-expru) | EXPRU | Group | Yes | No |[Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088)|
| [Attention Weighted Rank Fairness](https://kcachel.github.io/fairranktune/Metrics/#attention-weighted-rank-fairness-awrf) | AWRF | Group | No | Yes |[Sapiezynski et al.](https://dl.acm.org/doi/10.1145/3308560.3317595)  |
| [Exposure Rank Biased Precision Equality](https://kcachel.github.io/fairranktune/Metrics/#exposure-rank-biased-precision-equality-erbe) | ERBE | Group | No | No | [Kirnap et al.](https://dl.acm.org/doi/abs/10.1145/3442381.3450080)  |
| [Exposure Rank Biased Precision Proportionality](https://kcachel.github.io/fairranktune/Metrics/#exposue-rank-biased-precision-proportionality-erbp) | ERBP | Group | No | Yes | [Kirnap et al.](https://dl.acm.org/doi/abs/10.1145/3442381.3450080) |
| [Exposure Rank Biased Precision Proportional to Relevance](https://kcachel.github.io/fairranktune/Metrics/#exposure-rank-biased-precision-proportional-to-relevance-erbr) | ERBR | Group | Yes | No | [Kirnap et al.](https://dl.acm.org/doi/abs/10.1145/3442381.3450080) |
| [Attribute Rank Parity](https://kcachel.github.io/fairranktune/Metrics/#attribute-rank-parity-arp) | ARP | Group | No | Yes | [Cachel et al.](https://ieeexplore.ieee.org/document/9835646) |
| [Normalized Discounted KL-Divergence](https://kcachel.github.io/fairranktune/Metrics/#normalized-discounted-kl-divergence-ndkl) | NDKL | Group | No | Yes |[Geyik et al.](https://dl.acm.org/doi/10.1145/3292500.3330691)  |
| [Inequity of Amortized Attention](https://kcachel.github.io/FairRankTune/Metrics/#inequity-of-amortized-attention-iaa) | IAA | Individual | Yes | No | [Biega et al.](https://dl.acm.org/doi/10.1145/3209978.3210063)  |

Please refer to the [Metrics documentation](https://kcachel.github.io/fairranktune/Metrics/) for further details. 

### ⚖️ Fair Ranking Methods

```FairRankTune``` provides several [fair ranking algorithms](https://kcachel.github.io/fairranktune/Rankers/#supported-fair-ranking-algorithms) in the ```Rankers``` module. The [DetConstSort](https://kcachel.github.io/fairranktune/Rankers/#detconstsort-re-ranker) and [Epsilon-Greedy](https://kcachel.github.io/fairranktune/Rankers/#epsilon-greedy-re-ranker) fair ranking algorithms can be used to re-rank a given ranking with the objective of making the resulting ranking fair. 

Please refer to the [documentation](https://kcachel.github.io/fairranktune/Metrics/) for further details. 

## 🔌 Requirements
```bash
python>=3.8
```
As of `v.0.0.6`, [FairRankTune](https://github.com/KCachel/fairranktune) requires `python>=3.8`.

## 💾 Installation 

```bash
pip install FairRankTune
```

## 💡 Usage



### 🎨 Fairness-Aware Ranked Data Generation


```RankTune``` can be used to generate ranking(s) from ```group_proportions```, a numpy array with each group's proportion of the total items,```num_items```, by using the ```GenFromGroups()``` function.

```python title="GenFromGroups() function" hl_lines="12"
import FairRankTune as frt
import numpy as np
import pandas as pd
from FairRankTune import RankTune, Metrics

#Generate a biased (phi = 0.1) ranking of 1000 items, with four groups of 100, 200, 300, and 400 items each.
group_proportions = np.asarray([.1, .2, .3, .4]) #Array of group proportions
num_items = 1000 #1000 items to be in the generated ranking
phi = 0.1
r_cnt = 1 #Generate 1 ranking
seed = 10 #For reproducibility
ranking_df, item_group_dict = frt.RankTune.GenFromGroups(group_proportions, num_items, phi, r_cnt, seed)

#Calculate EXP with a MinMaxRatio
EXP_minmax, avg_exposures_minmax = frt.Metrics.EXP(ranking_df, item_group_dict, 'MinMaxRatio')
print("EXP of generated ranking: ", EXP_minmax, "avg_exposures: ", avg_exposures_minmax)
```

Output:
```python
EXP of generated ranking:  0.511665941043515 avg_exposures:  {0: 0.20498798214669187, 1: 0.13126425437156242, 2: 0.11461912123646827, 3: 0.10488536878769836}
```
Can confirm this is an unfair ranking by the low EXP value.


```RankTune``` can be used to generate ranking(s) from ```item_group_dict```, a dictionary of items where the keys are each item's group by using the ```GenFromItems()``` function.


```python title="GenFromItems() function" hl_lines="11"
import FairRankTune as frt
import numpy as np
import pandas as pd
from FairRankTune import RankTune, Metrics

#Generate a biased (phi = 0.1) ranking
item_group_dict = dict(Joe= "M",  David= "M", Bella= "W", Heidi= "W", Amy = "W", Jill= "W", Jane= "W", Dave= "M", Nancy= "W", Nick= "M")
phi = 0.1
r_cnt = 1 #Generate 1 ranking
seed = 10 #For reproducibility
ranking_df, item_group_dict = frt.RankTune.GenFromItems(item_group_dict, phi, r_cnt, seed)

#Calculate EXP with a MinMaxRatio
EXP_minmax, avg_exposures_minmax = frt.Metrics.EXP(ranking_df, item_group_dict, 'MinMaxRatio')
print("EXP of generated ranking: ", EXP_minmax, "avg_exposures: ", avg_exposures_minmax)
```

Output:
```python
EXP of generated ranking:  0.5158099476966725 avg_exposures:  {'M': 0.6404015779112127, 'W': 0.33032550440724917}
```
We can confirm this is a biased ranking base don the low EXP score and large difference in average exposure between the 'M' and 'W' groups.

For further detail on how to use ```RankTune``` to generate relevance scores see the [RankTune documentation](https://kcachel.github.io/fairranktune/RankTune/).

### 📏 Metrics
```python
import FairRankTune as frt
import pandas as pd
import numpy as np
ranking_df = pd.DataFrame(["Joe", "Jack", "Nick", "David", "Mark", "Josh", "Dave",
                          "Bella", "Heidi", "Amy"])
item_group_dict = dict(Joe= "M",  David= "M", Bella= "W", Heidi= "W", Amy = "W", Mark= "M", Josh= "M", Dave= "M", Jack= "M", Nick= "M")
#Calculate EXP with a MaxMinDiff
EXP, avg_exposures = frt.Metrics.EXP(ranking_df, item_group_dict, 'MaxMinDiff')
print("EXP: ", EXP, "avg_exposures: ", avg_exposures)
```
Output:
```python
>>> EXP:  0.21786100126614577 avg_exposures:  {'M': 0.5197142341886783, 'W': 0.3018532329225326}
```


### ⚖️ Fair Ranking Algorithms

```python title="Epsilon-Greedy Algorithm" 
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
We can see that the EXP fairness score improved from running Epsilon-Greedy. For more usage examples please see the [documentation](https://kcachel.github.io/fairranktune/Rankers/).

## 📖 Examples


| Topic | Link |
| :--- | :---|
| Quickstart | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KCachel/fairranktune/blob/main/examples/1_quickstart.ipynb) |
| RankTune Overview | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KCachel/fairranktune/blob/main/examples/2_ranktune.ipynb) |
| RankTune Augmenting Datasets | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KCachel/fairranktune/blob/main/examples/3_ranktune_augment.ipynb) |
| Statistical Parity Metrics | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KCachel/fairranktune/blob/main/examples/4_statisticalparitymetrics.ipynb) |
| Score-based (Group & Individual) Metrics | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KCachel/fairranktune/blob/main/examples/5_scorebasedmetrics.ipynb) |
| Using Fair Ranking Algorithms| [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KCachel/fairranktune/blob/main/examples/5_scorebasedmetrics.ipynb) |


## 📚 Documentation
Check out the [documentation](https://kcachel.github.io/fairranktune) for more details and example notebooks.


## 🎓 Citation
If you end up using [FairRankTune](https://github.com/KCachel/fairranktune) in your work, please consider citing it:
<details>
  <summary>BibTeX</summary>
  
  ```bibtex
  @misc{CachelFRT,
    author    = {Kathleen Cachel},
    title     = {FairRankTune: A Python Library for Fair Ranking},
    year = {2023},
    publisher = {GitHub},
    howpublished = {\url{https://github.com/KCachel/fairranktune}}
  }
  ```
</details>



## ⁉️ Feature Requests
We believe in open-source community driven software. Would you like to see other functionality implemented? Please, open a [feature request](https://github.com/KCachel/fairranktune/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=%5BFeature+Request%5D+title). Is there a bug or issue ? Please, open a [github issue](https://github.com/KCachel/fairranktune/issues/new).


## 👋 Want to contribute?
Would you like to contribute? Please, send me an [e-mail](mailto:kathleen.cachel@gmail.com?subject=[GitHub]%20fairranktune).


## 📄 License
[FairRankTune](https://github.com/KCachel/fairranktune) is open-sourced software licensed under the [BSD-3-Clause](https://github.com/KCachel/fairranktune/blob/main/LICENSE) license.