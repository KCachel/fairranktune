import numpy as np
import copy


def episilongreedy(current_ranking, current_group_ids, current_ranking_scores, epsilon, seed):
    """
    Epsilon-Greedy reranking algorithm.
    :param current_ranking: Numpy array of items to rerank.
    :param epsilon: Float epsilon value in [0,1].
    :param seed: Random seed value for reproducability.
    :return: reranking, Numpy array of item, reranking_ids, Numpy array of group ids for reranking, Numpy array of scores for reranking,
    """
    ranking = list(current_ranking)
    curr_ranking = copy.deepcopy(ranking)
    np.random.seed(seed) #for reproducibility
    reranking = []
    for i in range(len(curr_ranking)):
        p = np.random.rand()
        if p <= epsilon and i < len(curr_ranking) - 1: #swap items & can't swap last item
            temp = curr_ranking[i]
            j = np.random.randint(i+1, len(curr_ranking))
            curr_ranking[i] = curr_ranking[j]
            curr_ranking[j] = temp
            reranking.append(curr_ranking[i])
        else: #keep original ranking
            reranking.append(curr_ranking[i])

    reranking = np.asarray(reranking)
    reranking_scores = np.asarray([current_ranking_scores[ranking.index(item)] for item in reranking])
    reranking_ids = np.asarray([current_group_ids[ranking.index(item)] for item in reranking])
    return reranking, reranking_ids, reranking_scores