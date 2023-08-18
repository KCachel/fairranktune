# Home

<div align="center">
  <img src="https://raw.githubusercontent.com/KCachel/FairRankTune/main/.github/images/FairRankTune.png">
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

## ⚡️ Introduction

[FairRankTune](https://github.com/KCachel/FairRankTune) is a  an open-source [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) toolkit supporting end-to-end fair ranking workflows, analysis, auditing, and experimentation. FairRankTune provides researchers, practitioners, and educators with a self-contained module for generating ranked data, ranking strategies, and popular ranking-based fairness metrics.

For a quick overview, follow the [Usage](#-usage) section.

For a in-depth overview, follow the [Examples](#-examples) section.


## ✨ Features


### 🎨 Fairness-Aware Data Generation



Please refer to the [Metrics documentation](https://kcachel.github.io/FairRankTune/Metrics/) for further details. 

### 📏 Metrics

```FairRankTune ``` provides several metrics for evaluating the fairness of ranked lists in the ```Metrics``` module. The table below provides a high-level overview of each metric. These metrics encompass a variety of fair ranking metrics, including both [group](https://en.wikipedia.org/wiki/Fairness_(machine_learning)#Group_Fairness_criteria) and [individual](https://en.wikipedia.org/wiki/Fairness_(machine_learning)#Individual_Fairness_criteria) fairness, along with both score-based and statistical parity metrics. 


| **Metric** | **Abbreviation** | **Fairness (Group or Individual)** | **Score-based** | **Statistical Parity** | **Reference** |
|---|:---:|:---:|:---:|:---:|:---:|
| [Group Exposure](https://kcachel.github.io/FairRankTune/Metrics/#group-exposure-exp) | EXP | Group | No | Yes | [Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088) |
| [Exposure Utility](https://kcachel.github.io/FairRankTune/Metrics/#exposure-realized-utility-expru) | EXPU | Group | Yes | No | [Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088) |
| [Exposure Realized Utility](https://kcachel.github.io/FairRankTune/Metrics/#exposure-realized-utility-expru) | EXPRU | Group | Yes | No |[Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088)|
| [Attention Weighted Rank Fairness](https://kcachel.github.io/FairRankTune/Metrics/#attention-weighted-rank-fairness-awrf) | AWRF | Group | No | Yes |[Sapiezynski et al.](https://dl.acm.org/doi/10.1145/3308560.3317595)  |
| [Exposure Rank Biased Precision Equality](https://kcachel.github.io/FairRankTune/Metrics/#exposure-rank-biased-precision-equality-erbe) | ERBE | Group | No | No | [Kirnap et al.](https://dl.acm.org/doi/abs/10.1145/3442381.3450080)  |
| [Exposure Rank Biased Precision Proportionality](https://kcachel.github.io/FairRankTune/Metrics/#exposue-rank-biased-precision-proportionality-erbp) | ERBP | Group | No | Yes | [Kirnap et al.](https://dl.acm.org/doi/abs/10.1145/3442381.3450080) |
| [Exposure Rank Biased Precision Proportional to Relevance](https://kcachel.github.io/FairRankTune/Metrics/#exposure-rank-biased-precision-proportional-to-relevance-erbr) | ERBR | Group | Yes | No | [Kirnap et al.](https://dl.acm.org/doi/abs/10.1145/3442381.3450080) |
| [Attribute Rank Parity](https://kcachel.github.io/FairRankTune/Metrics/#attribute-rank-parity-arp) | ARP | Group | No | Yes | [Cachel et al.](https://ieeexplore.ieee.org/document/9835646) |
| [Normalized Discounted KL-Divergence](https://kcachel.github.io/FairRankTune/Metrics/#normalized-discounted-kl-divergence-ndkl) | NDKL | Group | No | Yes |[Geyik et al.](https://dl.acm.org/doi/10.1145/3292500.3330691)  |
| [Inequity of Amortized Attention](https://kcachel.github.io/FairRankTune/Metrics/#inequity-of-amortized-attention-iaa) | IAA | Individual | Yes | No | [Biega et al.](https://dl.acm.org/doi/10.1145/3209978.3210063)  |

Please refer to the [Metrics documentation](https://kcachel.github.io/FairRankTune/Metrics/) for further details. 

### ⚖️ Fair Ranking Methods


## 🔌 Requirements
```bash
python>=3.8
```
As of `v.0.0.1`, [FairRankTune](https://github.com/KCachel/FairRankTune) requires `python>=3.8`.

## 💾 Installation 

```bash
pip install FairRankTune
```

## 💡 Usage

### 🎨 Fairness-Aware Data Generation
```python
from FairRankTune import RankTune
```

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
```python
from FairRankTune import Rankers
```

## 📖 Examples

Include links.

## 📚 Documentation
Check out the [documentation](https://kcachel.github.io/FairRankTune) for more details and example notebooks.


## 🎓 Citation
If you end up using [FairRankTune](https://github.com/KCachel/FairRankTune) for conducting the experiments in your work, please consider citing it:
<details>
  <summary>BibTeX</summary>
  
  ```bibtex
  @misc{CachelFRT,
    author    = {Kathleen Cachel},
    title     = {FairRankTUne: A Python Library for Fair Ranking},
    year = {2023},
    publisher = {GitHub},
    howpublished = {\url{https://github.com/KCachel/FairRankTune}}
  }
  ```
</details>



## 🎁 Feature Requests
Would you like to see other functionality implemented? Please, open a [feature request](https://github.com/KCachel/FairRankTune/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=%5BFeature+Request%5D+title).


## 🤘 Want to contribute?
Would you like to contribute? Please, send me an [e-mail](mailto:kathleen.cachel@gmail.com?subject=[GitHub]%20fairranktune).


## 📄 License
).