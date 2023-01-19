import numpy as np
from timeit import timeit
from matplotlib import pyplot as plt
from pathlib import Path
import aigeanpy.clustering_numpy
import aigeanpy.clustering


# Version of cluster with numpy
def with_np(data: np.ndarray, clusters: int = 3, iterations: int = 10):
    """
    Perform the numpy version where return is unnecessary

    Parameters
    ----------
    data: np.ndarray
        Dataset loaded from the csv file, which is an array

    clusters : int, optional
        Number of clusters to divide the dataset into, default is 3

    iterations : int, optional
        Number of iterations to upload the centres, default is 10
    """
    alloc, centres = aigeanpy.clustering_numpy.cluster(data, clusters, iterations)
    pass


# Version of cluster without numpy
def without_np(data: np.ndarray, clusters: int = 3, iterations: int = 10):
    """
    Perform the without numpy version where return is unnecessary

    Parameters
    ----------
    data : np.ndarray
        Dataset loaded from the csv file, which is an array

    clusters : int, optional
        Number of clusters to divide the dataset into, default is 3

    iterations : int, optional
        Number of iterations to upload the centres, default is 10
    """
    alloc, centres = aigeanpy.clustering.cluster(data, clusters, iterations)
    pass


# Compare the performance of above two function
def save_figure(filename: Path):
    """
    Load dataset from the csv file and use those data to measure the performance

    Parameters
    ----------
    filename : Path
        A given Path, such as '../aigeanpy/samples.csv'
    """
    T_np, T_non = np.zeros(10), np.zeros(10)
    data = aigeanpy.clustering_numpy.load_data(filename)
    # Enlarge dataset by 30 times
    data_full = np.array(list(data) * 34)
    # Set ten different sizes of dataset.
    N = np.linspace(100, 10000, 10, dtype=int)
    for i in range(10):
        T_np[i] = timeit(lambda: with_np(data_full[:N[i]]), number=1)
        T_non[i] = timeit(lambda: without_np(data_full[:N[i]]), number=1)

    # Using a single plot for both versions
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
    save_figure(Path('../aigeanpy/samples.csv'))
