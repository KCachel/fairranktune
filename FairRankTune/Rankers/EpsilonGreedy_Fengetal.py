import numpy as np
import copy
import pandas as pd

# References: Feng, Y., & Shah, C. (2022, June).
# Has CEO gender bias really been fixed? adversarial attacking and improving gender fairness in image search.
# In Proceedings of the AAAI Conference on Artificial Intelligence (Vol. 36, No. 11, pp. 11882-11890).


def EPSILONGREEDY(
    current_ranking_df, item_group_dict, current_ranking_scores_df, epsilon, seed
):
    """
    Epsilon-Greedy reranking algorithm.
    :param current_ranking_df: Pandas dataframe of ranking to be reranked.
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param current_ranking_scores_df: Pandas dataframe of relevance scores associated with each item in the ranking.
    :param epsilon: Float epsilon value in [0,1].
    :param seed: Random seed value for reproducibility.
    :return: reranking, Pandas dataframe of items,item_group_reranked_dict, dictionary of items and group membership,  Pandas dataframe  of scores for reranking,
    """

    # Convert dataframes to numpy arrays
    current_ranking = current_ranking_df[0].to_numpy()
    current_group_ids = np.asarray([item_group_dict[i] for i in current_ranking])
    current_ranking_scores = current_ranking_scores_df[0].to_numpy()

    ranking = list(current_ranking)
    curr_ranking = copy.deepcopy(ranking)
    np.random.seed(seed)  # for reproducibility
    reranking = []
    for i in range(len(curr_ranking)):
        p = np.random.rand()
        if (
            p <= epsilon and i < len(curr_ranking) - 1
        ):  # swap items & can't swap last item
            temp = curr_ranking[i]
            j = np.random.randint(i + 1, len(curr_ranking))
            curr_ranking[i] = curr_ranking[j]
            curr_ranking[j] = temp
            reranking.append(curr_ranking[i])
        else:  # keep original ranking
            reranking.append(curr_ranking[i])

    reranking = np.asarray(reranking)
    reranking_scores = np.asarray(
        [current_ranking_scores[ranking.index(item)] for item in reranking]
    )
    reranking_ids = np.asarray(
        [current_group_ids[ranking.index(item)] for item in reranking]
    )
    item_group_reranked_dict = dict(zip(reranking, reranking_ids))
    return (
        pd.DataFrame(reranking),
        item_group_reranked_dict,
        pd.DataFrame(reranking_scores),
    )
