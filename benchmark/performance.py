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


def save_figure(filename):
    T_np, T_non = np.zeros(10), np.zeros(10)
    data = clustering_numpy.load_data(filename)
    data_full = np.array(list(data) * 34)
    N = np.linspace(100, 10000, 10, dtype=int)
    for i in range(10):
        T_np[i] = timeit(lambda: with_np(data_full[:N[i]]), number=1)
        T_non[i] = timeit(lambda: without_np(data_full[:N[i]]), number=1)

    plt.figure()
    plt.scatter(N, T_np)
    plt.plot(N, T_np, label='clustering_numpy')
    plt.scatter(N, T_non)
    plt.plot(N, T_non, 'r-', label='clustering')
    plt.title('Performance for versions with and without NumPy')
    plt.xlabel('Number of points N')
    plt.ylabel('Time required T')
    plt.legend()
    save_name = 'performance.png'
    plt.savefig(save_name)


if __name__ == "__main__":
    save_figure('../samples.csv')
