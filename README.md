# FairRankTune
Repository corresponding to the paper "FairRankTune: "

**Note, the Anonymous 4 open science program does NOT carry over the links below in all instances. To view the file please click on it in the navigation pane.**
## Table of Contents
1. [Basic installation instructions](#basic-installation-instructions)
2. [Quick start & notebook playground](#quick-start-playground)
3. [FairRankTune source](#fairranktune-source)
4. [Reproducing experiments](#reproducing-experiments)
5. [Plotting experimental results](#plotting-experimental-results)


## Basic Installation Instructions
1. Install via pip (note this is not available due to anonymized review. Once we can we will make fairranktune a pypi package).
```python
pip install FairRankTune
```
Or install directly from source (right now please download from the anonymous.4open.science repository).
```python
git clone <repo>
```
2. To use the generator you need to import the function from the package:
```python
import FairRankTune as rt
```

## Quick Start Playground
To use FairRankTune in your run:
```python
import FairRankTune as frt
import numpy as np #helpful to use
```

To generate a ranking with only the group distribution, number of items, and phi

```python
num_items = 1000
phi = 1  # maximally unfair
group_proportions = np.array([0.2, .3, .5])  # groups of size 200, 300, and 500
ranking, group_ids_in_ranking = frt.GenFromGroups(group_proportions, num_items, phi, 1)
```

To help get a feel for using FairRankTune we have created a self-contained notebook that includes the FairRankTune source code and metrics. To interact with FairRankTune please see [FairRankTunePlayground.ipynb](https://github.com/KCachel/FairRankTune/blob/main/FairRankTunePlayground.ipynb).



## FairRankTune Source
All source code for FairRankTune can be found in the [FAIRRANKTUNE](https://github.com/KCachel/FairRankTune/tree/main/FairRankTune) directory. Each of the three components of the toolkit have their own sub-package/directory described below.


#### RankTune
The RankTune source code is the [RankTune](https://github.com/KCachel/FairRankTune/tree/main/FairRankTune/RankTune) directory and correpsonding src.py script. 

#### Metrics
All metrics are in the *Metrics* directory. Each metric has a corresponding python script. 
- [ARP](https://github.com/KCachel/FairRankTune/blob/main/FairRankTune/Metrics/ARP.py) [1]
- [AWRF](https://github.com/KCachel/FairRankTune/blob/main/FairRankTune/Metrics/AWRF.py) [2]
- [ER](https://github.com/KCachel/FairRankTune/blob/main/FairRankTune/Metrics/ER.py) [3, 4]
- [NDKL](https://github.com/KCachel/FairRankTune/blob/main/FairRankTune/Metrics/NDKL.py) [5]

Functions to combine per-group metrics into a single metric are in the ComboUtil.py script. 

#### Rankers
All fair ranking methods are in the *Rankers* directory. Each method has a corresponding python script. 
- [DetConSort](https://github.com/KCachel/FairRankTune/blob/main/FairRankTune/Rankers/DetConSort_Geyiketal.py) [6]
- [Epsilon-Greedy](https://github.com/KCachel/FairRankTune/blob/main/FairRankTune/Rankers/EpsilonGreedy_Fengetal.py) [7]

Functions to combine per-group metrics into a single metric are in the ComboUtil.py script. 

## Reproducing Demonstration, Case Study, and Comparisons
The scripts to reproduce empirical analysis in the paper can be found in the [Analysis](https://github.com/KCachel/FairRankTune/tree/main/Analysis) directory along with the raw csv files containing the results. 

Law Demonstration: the [law](https://github.com/KCachel/FairRankTune/tree/main/Analysis/law) directory contains the law student data, scripts to run the experiment, result csv, and R script to generate the plots from the paper.

Comparison of RankTune to available methods: the [comparison](https://github.com/KCachel/FairRankTune/tree/main/Analysis/comparison) directory contains scripts for the compared methods, and the result csvs of running the data generation methods. 

Case Study: the [case_study](https://github.com/KCachel/FairRankTune/tree/main/Analysis/case_study) directory contains scripts and results from generating data and analyzing metrics on the nine distributions from the paper

Timing: the [timing](https://github.com/KCachel/FairRankTune/tree/main/Analysis/timing) directory contains the scripts and results from analyszing the runtime of RankTune.

### Generating plots from the paper
The scripts to generate the plots from the case study and comparison with URG are included in the [plotting.R](https://github.com/KCachel/FairRankTune/blob/main/plotting.R) file. This script saves off figures to the 'plots' folder in the main directory.

### References
[1] Cachel, K., Rundensteiner, E., & Harrison, L. (2022, May). Mani-rank: Multiple attribute and intersectional group fairness for consensus ranking. In 2022 IEEE 38th International Conference on Data Engineering (ICDE) (pp. 1124-1137). IEEE.

[2] Sapiezynski, P., Zeng, W., E Robertson, R., Mislove, A., & Wilson, C. (2019, May). Quantifying the impact of user attentionon fair group representation in ranked lists. In Companion proceedings of the 2019 world wide web conference (pp. 553-562).

[3] Diaz, F., Mitra, B., Ekstrand, M. D., Biega, A. J., & Carterette, B. (2020, October). Evaluating stochastic rankings with expected exposure. In Proceedings of the 29th ACM international conference on information & knowledge management (pp. 275-284).

[4] Singh, A., & Joachims, T. (2018, July). Fairness of exposure in rankings. In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (pp. 2219-2228).

[5] Geyik, S. C., Ambler, S., & Kenthapadi, K. (2019, July). Fairness-aware ranking in search & recommendation systems with application to linkedin talent search. In Proceedings of the 25th acm sigkdd international conference on knowledge discovery & data mining (pp. 2221-2231).

[6] Yang, K., & Stoyanovich, J. (2017, June). Measuring fairness in ranked outputs. In Proceedings of the 29th international conference on scientific and statistical database management (pp. 1-6).