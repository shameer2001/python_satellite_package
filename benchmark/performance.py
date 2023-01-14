import numpy as np
from timeit import timeit
from matplotlib import pyplot as plt
import sys

sys.path.append('..')
import clustering_numpy
import clustering


def with_np(data: np.array, clusters: int = 3, iterations: int = 10):
    alloc, centres = clustering_numpy.cluster(data, clusters, iterations)
    pass


def without_np(data: np.array, clusters: int = 3, iterations: int = 10):
    alloc, centres = clustering.cluster(data, clusters, iterations)
    pass


T_np, T_non = np.zeros(10), np.zeros(10)
data = clustering_numpy.load_data('../samples.csv')
data_full = np.array(list(data) * 34)
N = np.linspace(100, 10000, 10, dtype=int)
for i in range(10):
    T_np[i] = timeit(lambda: with_np(data_full[:N[i]]), number=1)
    T_non[i] = timeit(lambda: without_np(data_full[:N[i]]), number=1)
