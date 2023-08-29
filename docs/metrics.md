# Metrics

## Overview
```FairRankTune ``` provides several metrics for evaluating the fairness of ranked lists in the ```Metrics``` module. The table below provides a high-level overview of each metric. These metrics encompass a variety of fair ranking metrics, including both [group](https://en.wikipedia.org/wiki/Fairness_(machine_learning)#Group_Fairness_criteria) and [individual](https://en.wikipedia.org/wiki/Fairness_(machine_learning)#Individual_Fairness_criteria) fairness, along with both score-based and statistical parity metrics. 

>What is group, individual, score-based, and or statistical parity fairness? 

*Group Fairness*: Measures if groups of items are being treated similarly. For example, we might want to know if groups are making it to the top of ranking(s).

*Individual Fairness*: Measures if similar items are being treated similarly. For example, we might want to know if items that are similar are ranked in similar positions in rankings.

*Score-based Fairness*: Measures if exposure (or attention, clicks, views etc.) are proportional to item relevance or group relevance. For example, in the form of individual fairness, we might want to know if items that are similar received similar amounts of exposure in rankings. Or for group fairness, we might want to know if groups are click-on proportional to their relevance.

*Statistical Parity Fairness*: A sub-type of *Group Fairness*, measures if groups receive a proportional share of the positive outcome; in ranking(s) the positive outcome can be the exposure or attention of the viewer or a share of top-ranked position. Statistical Parity is also known as Demographic Parity and explicitly does not use relevance scores. For example, we might want to know if groups receive comparable amounts of exposure.

| **Metric** | **Abbreviation** | **Fairness (Group or Individual)** | **Score-based** | **Statistical Parity** | **Reference** |
|---|:---:|:---:|:---:|:---:|:---:|
| [Group Exposure](#group-exposure-exp) | EXP | Group | No | Yes | [Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088) |
| [Exposure Utility](#exposure-realized-utility-expru) | EXPU | Group | Yes | No | [Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088) |
| [Exposure Realized Utility](#exposure-realized-utility-expru) | EXPRU | Group | Yes | No |[Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088)|
| [Attention Weighted Rank Fairness](#attention-weighted-rank-fairness-awrf) | AWRF | Group | No | Yes |[Sapiezynski et al.](https://dl.acm.org/doi/10.1145/3308560.3317595)  |
| [Exposure Rank Biased Precision Equality](#exposure-rank-biased-precision-equality-erbe) | ERBE | Group | No | No | [Kirnap et al.](https://dl.acm.org/doi/abs/10.1145/3442381.3450080)  |
| [Exposure Rank Biased Precision Proportionality](#exposue-rank-biased-precision-proportionality-erbp) | ERBP | Group | No | Yes | [Kirnap et al.](https://dl.acm.org/doi/abs/10.1145/3442381.3450080) |
| [Exposure Rank Biased Precision Proportional to Relevance](#exposure-rank-biased-precision-proportional-to-relevance-erbr) | ERBR | Group | Yes | No | [Kirnap et al.](https://dl.acm.org/doi/abs/10.1145/3442381.3450080) |
| [Attribute Rank Parity](#attribute-rank-parity-arp) | ARP | Group | No | Yes | [Cachel et al.](https://ieeexplore.ieee.org/document/9835646) |
| [Normalized Discounted KL-Divergence](#normalized-discounted-kl-divergence-ndkl) | NDKL | Group | No | Yes |[Geyik et al.](https://dl.acm.org/doi/10.1145/3292500.3330691)  |
| [Inequity of Amortized Attention](#inequity-of-amortized-attention-iaa) | IAA | Individual | Yes | No | [Biega et al.](https://dl.acm.org/doi/10.1145/3209978.3210063)  |


## Modular Metric Implementation

A key functionality of the  ```Metrics``` library in ```FairRankTune```  is providing toolkit users multiple choices for how to calculate a given top-level fairness metric. For instance, for group exposure,  a popular fairness criteria,  ```Metrics``` offers seven ways of calculating a top-level exposure metric (e.g., min-max ratios, max absolute difference, L-2 norms of per-group exposures, etc.).


Below are the formulas supported for combining per-group style metrics. In the formulas $V = [V_{1}, ..., V_{g}$] is an array of per-group metrics and $G$ is the number of groups. The ```combo``` variable is used directly in the function call. Depending on the formula used for aggregating per-group metrics the range of the given fairness metric varies. The range and its corresponding "most fair" value is provided in the table. 

| **Combo Variable in ```FairRankTune```** | **Formula** | **Range** | **Most Fair** | 
|---|:---:|:---:|:---:|
| ```MinMaxRatio``` |  $min_{g} V / max_{g} V$ | [0,1] | 1 |
| ```MaxMinRatio``` |  $max_{g} V / min_{g} V$ | [1, $\infty$] | 1 |
| ```MaxMinDiff``` |  $max_{g} V - min_{g} V$ |  [0,1] | 0 |
| ```MaxAbsDiff``` | $max_{g} \mid V - V_{mean} \mid$ |  [0, $\infty$] | 0 |
| ```MeanAbsDev``` | $\frac{1}{G} \sum_{g} \mid V - V_{mean}\mid$ | [0, $\infty$] | 0 |
| ```LTwo```| $\lVert V \rVert_2^2$ | [0, $\infty$] | 0 |
|  ```Variance``` |  $\frac{1}{G - 1} \sum_{g} (V_{g} - V_{mean})^2$ | [0, $\infty$] | 0 |


Usage:

```python
from FairRankTune import RankTune, Metrics
import random
random.seed(10)

#Generate a biased (phi = 0) ranking of 1000 items, with two groups of 100 and 900 items each. 
ranking_df, item_group_dict = frt.RankTune.GenFromGroups(np.asarray([.1, .9]),  1000, 0, 1)

#Calculate EXP with a MinMaxRatio
EXP_minmax, avg_exposures_minmax = frt.Metrics.EXP(ranking_df, item_group_dict, 'MinMaxRatio')
print("EXP_minmax: ", EXP_minmax, "avg_exposures: ", avg_exposures)
#Calculate EXP with a MaxAbsDiff
EXP_maxabs, avg_exposures_maxabs = frt.Metrics.EXP(ranking_df, item_group_dict, 'MaxAbsDiff')
print("EXP_maxabs: ", EXP_maxabs, "avg_exposures: ", avg_exposures)
```
Outputs:
```python
EXP_minmax:  0.5420744267551784 avg_exposures:  {0: 0.2093867087428094, 1: 0.11350318011191189}
EXP_maxabs:  0.04794176431544876 avg_exposures:  {0: 0.2093867087428094, 1: 0.11350318011191189}
```
Notice that the ```EXP_minmax``` and ```EXP_maxabs``` are different. The second returned object is a dictionary with groups as keys and the values represent the per-group metric. In this example that is the average exposure of group 0 and group 1.

The following metrics have meta-metric functionality: [EXP](#group-exposure-exp), [EXPU](#exposure-utility-expu), [EXRU](#exposure-realized-utility-expru), [AWRF](#attention-weighted-rank-fairness-awrf), [ERBE](#exposure-rank-biased-precision-equality-erbe), [ERBP](#exposue-rank-biased-precision-proportionality-erbp), [ERBPR](#exposure-rank-biased-precision-proportional-to-relevance-erbr), and [ARP](#attribute-rank-parity-arp). To specify the desired aggregation form pass any of the strings in the table above as the  ```combo``` input variable. 

## Supported Fair Ranking Metrics

All metric functions take as the inputted ```ranking_df``` parameter a [pandas dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) of the ranking(s) to be evaluated. These rankings need not have the same number of items, and items can be represented as floats, ints, or strings.

All group fairness metric functions take as the inputted ```item_group_dict``` parameter a [python dictionary](https://realpython.com/python-dicts/) of items and their group membership. Items are keys, and the value represents the group of that item (ints or strings are equally fine). Note, that all group metrics supported in ```FairRankTune``` support multiple groups.


### Group Exposure (EXP)
EXP compares the average exposures of groups in the ranking(s) and does not consider relevances or scores associate with items. It aligns with the fairness concept of statistical parity. The per-group metric is the group average exposure, whereby the exposure of item $x_i$ in ranking $\tau$ is $exposure(\tau,x_i) = 1 / log_2(\tau(x_i)+1))$ and the average exposure for group $g_j$ is $avgexp(\tau,g_j) = \sum_{\forall x \in g_{j}}exposure(\tau,x_i)/|g_{j}|$. The range of EXP and its "most fair" value depends on the [per-group aggregation](#modular-metric-implementation) ```combo``` variable. 

Usage:

```python
#Calculate EXP with a MinMaxRatio
EXP_minmax, avg_exposures = frt.Metrics.EXP(ranking_df, item_group_dict, 'MinMaxRatio')
```
The first returned object is float specifying the EXP value and the second returned object is a dictionary of average exposures for each group (keys are group ids).

Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{10.1145/3219819.3220088,
author = {Singh, Ashudeep and Joachims, Thorsten},
title = {Fairness of Exposure in Rankings},
year = {2018},
isbn = {9781450355520},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3219819.3220088},
doi = {10.1145/3219819.3220088},
booktitle = {Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery \& Data Mining},
pages = {2219–2228},
numpages = {10},
keywords = {algorithmic bias, fairness, position bias, equal opportunity, fairness in rankings},
location = {London, United Kingdom},
series = {KDD '18}
}
```
</details>

Fairness of Group Exposure is also introduced in [Diaz et al.](https://dl.acm.org/doi/10.1145/3340531.3411962).

Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{10.1145/3340531.3411962,
author = {Diaz, Fernando and Mitra, Bhaskar and Ekstrand, Michael D. and Biega, Asia J. and Carterette, Ben},
title = {Evaluating Stochastic Rankings with Expected Exposure},
year = {2020},
isbn = {9781450368599},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3340531.3411962},
doi = {10.1145/3340531.3411962},
booktitle = {Proceedings of the 29th ACM International Conference on Information \& Knowledge Management},
pages = {275–284},
numpages = {10},
keywords = {fairness, evaluation, diversity, learning to rank},
location = {Virtual Event, Ireland},
series = {CIKM '20}
}
```
</details>

### Exposure Utility (EXPU)

EXPU assesses if groups receive exposure proportional to their relevance in the ranking(s). This is a form of group fairness that considers the scores (relevances) associated with items. The per-group metric is the ratio of group average exposure and group average utility, whereby group average exposure is measured exactly as in [EXP](#group-exposure-exp). Group average utility for group $g_j$ is $avgutil(\tau,g_j) = \sum_{\forall x \in g_{j}}x_i^{util_{\tau}}/|g_{j}|$, where $x_i^{util_{\tau}}$ is the utility (or relevance score) for candidate $x_i$ in ranking $\tau$.  The range of EXPU and its "most fair" value depends on the [per-group aggregation](#modular-metric-implementation) ```combo``` variable. 

[Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088) refer to EXPU as "Disparate Treatment", as pointed out by Raj et al. this terminology, is inconsistent with the use of these terms in the broader algorithmic fairness literature, thus ```FairRankTune``` uses the term "Exposure Utility" a introduced in [Raj et al.}(https://dl.acm.org/doi/10.1145/3477495.3532018).

Usage:


```python
#Calculate EXPU with a MinMaxRatio
EXPU, per_group = frt.Metrics.EXPU(ranking_df, item_group_dict, relevance_df, 'MinMaxRatio')
```
Note that the relevance scores associated with the ranking(s) in ```relevance_df``` must be between 0 and 1. The first returned object is a float specifying the EXPU value and the second returned object is a dictionary of average exposure and average utility ratios for each group (keys are group ids).

Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{10.1145/3219819.3220088,
author = {Singh, Ashudeep and Joachims, Thorsten},
title = {Fairness of Exposure in Rankings},
year = {2018},
isbn = {9781450355520},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3219819.3220088},
doi = {10.1145/3219819.3220088},
booktitle = {Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery \& Data Mining},
pages = {2219–2228},
numpages = {10},
keywords = {algorithmic bias, fairness, position bias, equal opportunity, fairness in rankings},
location = {London, United Kingdom},
series = {KDD '18}
}
```
</details>

### Exposure Realized Utility (EXPRU)

EXPRU assesses if groups are click-on proportional to their relevance in the ranking(s). This is a form of group fairness that considers the scores (relevances) associated with items. The per-group metric is the ratio of group average click-through rate and group average utility, whereby  group average utility is measured exactly as in EXPU. The average click-through rate for group $g_j$ in $\tau$ is $avgctr(\tau,g_j) = \sum_{\forall x \in g_{j}}x_i^{ctr_{\tau}}/|g_{j}|$, where $x_i^{ctr_{\tau}}$ is the click-through rate for candidate $x_i$ in ranking $\tau$.  The range of EXPRU and its "most fair" value depends on the [per-group aggregation](#modular-metric-implementation) ```combo``` variable. 

[Singh et al.](https://dl.acm.org/doi/10.1145/3219819.3220088) refer to EXPRU as "Disparate Impact", as pointed out by Raj et al. this terminology, is inconsistent with the use of these terms in the broader algorithmic fairness literature, thus ```FairRankTune``` uses the term "Exposure Realized Utility" a introduced in [Raj et al.](https://dl.acm.org/doi/10.1145/3477495.3532018).

Usage:
```python
#Calculate EXPRU with a MinMaxRatio
EXPRU, per_group = frt.Metrics.EXPRU(ranking_df, item_group_dict, relevance_df, ctr_df,'MinMaxRatio')
```
Note that the relevance scores associated with the ranking(s) in ```relevance_df``` must be between 0 and 1 and the click-through-rates in ```ctr_df``` must be between 0 (no clicks) or 1 (100% ctr). The first returned object is a float specifying the EXPRU value and the second returned object is a dictionary of  average utility and average click-through rate ratios for each group (keys are group ids).

Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{10.1145/3219819.3220088,
author = {Singh, Ashudeep and Joachims, Thorsten},
title = {Fairness of Exposure in Rankings},
year = {2018},
isbn = {9781450355520},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3219819.3220088},
doi = {10.1145/3219819.3220088},
booktitle = {Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery \& Data Mining},
pages = {2219–2228},
numpages = {10},
keywords = {algorithmic bias, fairness, position bias, equal opportunity, fairness in rankings},
location = {London, United Kingdom},
series = {KDD '18}
}
```
</details>

### Attention Weighted Rank Fairness (AWRF)

AWRF compares the average attention of groups in the ranking(s)and does not consider relevances or scores associate with items. It aligns with the fairness concept of statistical parity.  Attention compared to [exposure](#group-exposure-exp) uses a geometric discount on the "attention" assigned to positions in a ranking. The per-group metric is the group average attention,
whereby the attention score for item $x_i$ in ranking $\tau$ as $attention(\tau,x_i) = 100 \times (1 - p) ^{(\tau(x_i) -1)} \times p$, where $p$ is a parameter representing the proportion of attention received by the first (top) ranked item.  The range of AWRF and its "most fair" value depends on the [per-group aggregation](#modular-metric-implementation) ```combo``` variable. 


Usage:
```python
#Calculate AWRF with a MinMaxRatio
p = .01 #parameter representing the proportion of attention received by the first postion
AWRF, per_group = frt.Metrics.AWRF(ranking_df, item_group_dict, p, 'MinMaxRatio')
```
The first returned object is a float specifying the AWRF value and the second returned object is a dictionary of average attention values for each group (keys are group ids).


Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{10.1145/3308560.3317595,
author = {Sapiezynski, Piotr and Zeng, Wesley and E Robertson, Ronald and Mislove, Alan and Wilson, Christo},
title = {Quantifying the Impact of User Attention on Fair Group Representation in Ranked Lists},
year = {2019},
isbn = {9781450366755},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3308560.3317595},
doi = {10.1145/3308560.3317595},
pages = {553–562},
numpages = {10},
keywords = {group fairness, ranked lists, information retrieval},
location = {San Francisco, USA},
series = {WWW '19}
}
```
</details>

### Exposure Rank Biased Precision Equality (ERBE)

ERBE assesses if groups receive equal exposure whereby exposure is based on the Rank Biased Precision metric. This metric does not consider relevances or scores associate with items. Exposure in ERBE is determined differently compared to [exposure (EXP)](#group-exposure-exp). Specifically this calculation is based on the [Rank Biased Precision (RBP) metric](https://dl.acm.org/doi/10.1145/1416950.1416952). The per-group metric is the group RBP-based exposure, whereby the Rank Biased Precision exposure of item $x_i$ in ranking $\tau$ is $exposureRBP(\tau,x_i) = \gamma^{(1-\tau(x_i))}$ and the exposure for group $g_j$ is $expRBP(\tau,g_j) = (1 - \gamma) \sum_{\forall x \in g_{j}}exposureRBP(\tau,x_i)$.  The range of ERBE and its "most fair" value depends on the [per-group aggregation](#modular-metric-implementation) ```combo``` variable. 


Usage:
```python
#Calculate ERBE with a MinMaxRatio
decay = .01 #paramater representing gamma which controls the importance of higher ranks
ERBE, per_group = frt.Metrics.ERBE(ranking_df, item_group_dict, decay, 'MinMaxRatio')
```
The first returned object is a float specifying the ERBE value and the second returned object is a dictionary of total exposure values for each group (keys are group ids).


Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{10.1145/3442381.3450080,
author = {K\i{}rnap, \"{O}mer and Diaz, Fernando and Biega, Asia and Ekstrand, Michael and Carterette, Ben and Yilmaz, Emine},
title = {Estimation of Fair Ranking Metrics with Incomplete Judgments},
year = {2021},
isbn = {9781450383127},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3442381.3450080},
doi = {10.1145/3442381.3450080},
booktitle = {Proceedings of the Web Conference 2021},
pages = {1065–1075},
numpages = {11},
keywords = {fair ranking, evaluation, information retrieval, fairness},
location = {Ljubljana, Slovenia},
series = {WWW '21}
}
```
</details>

### Exposure Rank Biased Precision Proportionality (ERBP)

ERBP assesses if groups receive exposure proportional to their size whereby exposure is based on the Rank Biased Precision metric) This metric does not consider relevances or scores associate with items. Exposure in ERBE is determined differently compared to [exposure (EXP)](#group-exposure-exp). Specifically this calculation is based on the [Rank Biased Precision (RBP) metric](https://dl.acm.org/doi/10.1145/1416950.1416952).  The per-group metric is the group average exposure, whereby exposure is measured exactly as in [ERBE](#exposure-rank-biased-precision-equality-erbe). Group average exposure for group $g_j$ is $avgexpRBP(\tau,g_j) = (1 - \gamma) \sum_{\forall x \in g_{j}}exposureRBP(\tau,x_i)/|g_{j}|$.  The range of ERBP and its "most fair" value depends on the [per-group aggregation](#modular-metric-implementation) ```combo``` variable. 

Usage:
```python
#Calculate ERBP with a MinMaxRatio
decay = .01 #paramater representing gamma which controls the importance of higher ranks
ERBP, per_group = frt.Metrics.ERBP(ranking_df, item_group_dict, decay, 'MinMaxRatio')
```
The first returned object is a float specifying the ERBP value and the second returned object is a dictionary of average exposure values for each group (keys are group ids).
Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{10.1145/3442381.3450080,
author = {K\i{}rnap, \"{O}mer and Diaz, Fernando and Biega, Asia and Ekstrand, Michael and Carterette, Ben and Yilmaz, Emine},
title = {Estimation of Fair Ranking Metrics with Incomplete Judgments},
year = {2021},
isbn = {9781450383127},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3442381.3450080},
doi = {10.1145/3442381.3450080},
booktitle = {Proceedings of the Web Conference 2021},
pages = {1065–1075},
numpages = {11},
keywords = {fair ranking, evaluation, information retrieval, fairness},
location = {Ljubljana, Slovenia},
series = {WWW '21}
}
```
</details>

### Exposure Rank Biased Precision Proportional to Relevance (ERBR)

ERBR assesses if groups receive exposure proportional to how many relevant items are in the group. It aligns with the fairness concept of statistical parity. This is a form of group fairness that considers the scores (relevances) associated with items. The per-group metric is the ratio of group exposure and the number of items belonging to the given group that are relevant, whereby exposure is measured exactly as in ERBE. This ratio for group $g_j$ is $expRBP2rel(\tau,g_j) = (1 - \gamma) \sum_{\forall x \in g_{j}}exposureRBP(\tau,x_i)/|g_{j}^{rel}|$, where $|g_{j}^{rel}|$ is the count of relevant items in group $g_{j}$.  The range of ERBR and its "most fair" value depends on the [per-group aggregation](#modular-metric-implementation) ```combo``` variable. 

Usage:
```python
#Calculate ERBR with a MinMaxRatio
decay = .01 #paramater representing gamma which controls the importance of higher ranks
ERBR, per_group = frt.Metrics.ERBP(ranking_df, item_group_dict, relevance_df, decay, 'MinMaxRatio')
```
Note that the relevance scores associated with the ranking(s) in ```relevance_df``` must be either 0 or 1. The first returned object is float specifying the ERBR value and the second returned object is a dictionary of exposure and relevance ratios for each group (keys are group ids).

Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{10.1145/3442381.3450080,
author = {K\i{}rnap, \"{O}mer and Diaz, Fernando and Biega, Asia and Ekstrand, Michael and Carterette, Ben and Yilmaz, Emine},
title = {Estimation of Fair Ranking Metrics with Incomplete Judgments},
year = {2021},
isbn = {9781450383127},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3442381.3450080},
doi = {10.1145/3442381.3450080},
booktitle = {Proceedings of the Web Conference 2021},
pages = {1065–1075},
numpages = {11},
keywords = {fair ranking, evaluation, information retrieval, fairness},
location = {Ljubljana, Slovenia},
series = {WWW '21}
}
```
</details>

### Attribute Rank Parity (ARP)

ARP compares the number of mixed pairs won by groups in the ranking(s) and does not consider relevances or scores associate with items. It aligns with the fairness concept of statistical parity. ARP decomposes the ranking into pairwise comparisons, a mixed pair contains items from two different groups, the item "on top" is said to "win" the pair. The per-group metric is the average mixed pairs won by each group, calculated as $avgpairs(\tau, g_i) = \# ~mixedpairswon(g_i) / \# totalmixedpairs(g_i)$ in ranking $\tau$.  The range of ARP and its "most fair" value depends on the [per-group aggregation](#modular-metric-implementation) ```combo``` variable. 

Usage:
```python
#Calculate ARP with a MaxAbsDiff
decay = .01 #paramater representing gamma which controls the importance of higher ranks
ARP, per_group = frt.Metrics.ARP(ranking_df, item_group_dict,  'MaxAbsDiff')
```

The first returned object is a float specifying the ARP value and the second returned object is a dictionary of FPR scores (average count of won mixed pairs) for each group (keys are group ids).

Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{9835646,
  author={Cachel, Kathleen and Rundensteiner, Elke and Harrison, Lane},
  booktitle={2022 IEEE 38th International Conference on Data Engineering (ICDE)}, 
  title={MANI-Rank: Multiple Attribute and Intersectional Group Fairness for Consensus Ranking}, 
  year={2022},
  volume={},
  number={},
  pages={1124-1137},
  doi={10.1109/ICDE53745.2022.00089}}
```
</details>

### Normalized Discounted KL-Divergence (NDKL)

NDKL asseses the representation of groups in dsicrete prefixes of the ranking. It does not considers the relevance or scores associated with items. It aligns with the fairness cocnept of statistical parity and is assess on a single ranking. The NDKL of ranking $\tau$ with respect to groups $G$ is defined as:
$\frac{1}{Z}\sum^{|X|}_{i = 1}\frac{1}{log_{2}(i +1 )}d_{KL}(D_{\tau_i} || D_{X})$
where $d_{KL}(D_{\tau_i} || D_{X})$ is the [KL-divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) score of the group proportions of the first $i$ positions in $\tau$ and the group proportions of the item set $X$ and $Z = \sum_{i = 1}^{| \tau |} \frac{1}{log_2(i + 1)}$. NDKL ranges from 0 to $\infty$, and is most fair at 0.

Usage:
```python
#Calculate NDKL
NDKL= frt.Metrics.NDKL(ranking_df, item_group_dict)
```
The returned object is a float specifying the NDKL value.

Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{10.1145/3292500.3330691,
author = {Geyik, Sahin Cem and Ambler, Stuart and Kenthapadi, Krishnaram},
title = {Fairness-Aware Ranking in Search \& Recommendation Systems with Application to LinkedIn Talent Search},
year = {2019},
isbn = {9781450362016},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3292500.3330691},
doi = {10.1145/3292500.3330691},
booktitle = {Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery \& Data Mining},
pages = {2221–2231},
numpages = {11},
keywords = {fairness-aware ranking, talent search \& recommendation systems},
location = {Anchorage, AK, USA},
series = {KDD '19}
}
```
</details>

### Inequity of Amortized Attention (IAA)

IAA assess if a series of rankings is individually fair; meaning items are given attention similiar to their relevance. IAA measures the difference, via the $L_1$ norm between the cumulative attention and cumulative relevance of items in the rankings. Whereby the attention of an item $x_i$ in ranking $\tau$ is $attention(\tau,x_i) = 1 / log_2(\tau(x_i)+1))$ and the relevance of an item is a $[0 - 1]$-normalized score. IAA is ranges from 0 to $\infty$, and is most fair at 0.

Usage:
```python
#Calculate IAA
IAA = frt.Metrics.IAA(ranking_df, relevance_df)
```
Note that the relevance scores associated with the rankings in ```relevance_df``` must be between 0 and 1. The returned object is a float specifying the IAA value.

Citation:
<details>
  <summary>BibTeX</summary>
  
```bibtex
@inproceedings{10.1145/3209978.3210063,
author = {Biega, Asia J. and Gummadi, Krishna P. and Weikum, Gerhard},
title = {Equity of Attention: Amortizing Individual Fairness in Rankings},
year = {2018},
isbn = {9781450356572},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3209978.3210063},
doi = {10.1145/3209978.3210063},
booktitle = {The 41st International ACM SIGIR Conference on Research \& Development in Information Retrieval},
pages = {405–414},
numpages = {10},
keywords = {individual fairness, fair ranking, amortized fairness, exposure, algorithmic fairness, attention, position bias},
location = {Ann Arbor, MI, USA},
series = {SIGIR '18}
}
```
</details>
