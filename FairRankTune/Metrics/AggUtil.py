# Script containing methods to aggregate group-level metrics to meta-metrics
import numpy as np

def MinMaxRatio(vals):
    """
    Agg via min max ratio
    :param vals: numpy array of group level metrics
    :return: float score
    """
    return np.min(vals) /np.max(vals)

def MaxMinRatio(vals):
    """
    Agg via max min ratio
    :param vals: numpy array of group level metrics
    :return: float score
    """
    return np.max(vals) /np.min(vals)


def MaxMinDiff(vals):
    """
    Agg via max min difference
    :param vals: numpy array of group level metrics
    :return: float score
    """
    return np.max(vals) - np.min(vals)


def MaxAbsDiff(vals):
    """
    Agg via max absolute difference
    :param vals: numpy array of group level metrics
    :return: float score
    """
    mean = np.mean(vals)
    val = 0
    for i in range(0,len(vals)):
        v = vals[i]
        val_curr = np.abs(v - mean)
        if val_curr > val: val = val_curr
    return val

def MeanAbsDev(vals):
    """
        Agg via mean absolute difference
        :param vals: numpy array of group level metrics
        :return: float score
        """
    val = np.sum(np.abs(vals - np.mean(vals)))/len(vals)
    return val


def LTwo(vals):
    """
        Agg via L2 norm
        :param vals: numpy array of group level metrics
        :return: float score
        """
    return np.linalg.norm(vals, 2)


def Variance(vals):
    """
        Agg via variance
        :param vals: numpy array of group level metrics
        :return: float score
        """
    return np.var(vals)
