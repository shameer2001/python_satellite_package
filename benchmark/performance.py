import numpy as np
from timeit import timeit
from matplotlib import pyplot as plt
import sys
sys.path.append('..')
import clustering_numpy
import clustering


def with_np(data: np.array, clusters: int=3, iterations: int=10):
    alloc, centres = clustering_numpy.cluster(data, clusters, iterations)
    pass
