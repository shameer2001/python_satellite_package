import numpy as np
from pathlib import Path
from argparse import ArgumentParser


# Use numpy to load data.
def load_data(filepath: Path):
    """
    Loading data from csv file.

    Parameters
    ----------
    filepath : Path
        A given Path, such as "samples.csv"

    Returns
    -------
    data : np.array
        The data from the csv file.
    """
    data = np.loadtxt(filepath, dtype=float, delimiter=',')
    return data


# Add distance function to reduce repetition and for loops.
def distance(centres: np.array, points: np.array):
    """
    This function calculates the euclidean distance between each point from centres and each point from dataset
    and stores those distances in an array by using matrix product, which can reduce the usage of for loops and
    will not change the kmean algorithm itself.

    Parameters
    ----------
    centres: np.array
        A set of points which contains all centres

    points: np.array
        Dataset loaded from the csv file contains all points

    Returns
    -------
    mat_dist : np.matrix
        A matrix contains the euclidean distance D_ij which means it is the distance between point i in
        points and point j in centres.
    """
    n, _ = np.shape(centres)
    m, _ = np.shape(points)
    mat_A = np.tile(np.matrix(np.square(points).sum(axis=1)).T, (1, n))
    mat_B = np.tile(np.matrix(np.square(centres).sum(axis=1)), (m, 1))
    mat_C = points @ centres.T
    mat_dist = np.sqrt(abs(-2 * mat_C + mat_A + mat_B))
    return mat_dist


# Perform the kmean algorithm using numpy.
def cluster(data: np.array, clusters: int = 3, iterations: int = 10):
    """
    Use kmean algorithm (numpy version) to classify dataset provided.

    Parameters
    ----------
    data: np.array
        Dataset loaded from the csv file, which is an array

    clusters : int, optional
        Number of clusters to divide the dataset into, default is 3

    iterations : int, optional
        Number of iterations to upload the centres, default is 10

    Returns
    -------
    alloc : np.array
        Index of clusters where each points belong to

    centres : np.array
        The final centres for each cluster
    """
    num = len(data)
    k = clusters
    rand_index = np.random.randint(num, size=k)
    centres = data[rand_index]
    count = 0
    while count < iterations:
        # The new distance function can calculate all the distance at a time.
        dist_mat = distance(centres, data)
        alloc = np.array(np.argmin(dist_mat, axis=1).T)[0]
        for i in range(k):
            alloc_ps = np.array([p for j, p in enumerate(data) if alloc[j] == i])
            new_mean = np.array(np.sum(alloc_ps, axis=0) / len(alloc_ps))
            centres[i] = new_mean
        count = count + 1
    return alloc, centres


# Add a command-line interface
def process():
    parser = ArgumentParser(description="Generate clusters using kmean")
    # Add optional argument iters, default is 10.
    parser.add_argument('--iters', type=int, default=10)
    # Add optional argument clusters, default is 3.
    parser.add_argument('--clusters', type=int, default=3)
    # Add argument Path.
    parser.add_argument('Path')
    arguments = parser.parse_args()
    data = load_data(Path(f'{arguments.Path}'))
    alloc, centres = cluster(data, arguments.clusters, arguments.iters)
    k = len(centres)
    # Print the final result, where we do not use numpy to keep the output the same.
    for i in range(k):
        alloc_ps = [tuple(p) for j, p in enumerate(data) if alloc[j] == i]
        print("Cluster " + str(i) + " is centred at " + str(tuple(centres[i])) +
              " and has " + str(len(alloc_ps)) + " points.")
        print(alloc_ps)


if __name__ == "__main__":
    process()
