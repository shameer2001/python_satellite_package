from clustering_numpy import *
from pathlib import Path


# Add a function kmeans() to perform kmean algorithm on csv file provided.
def kmeans(filename: Path, clusters: int = 3, iterations: int = 10):
    """
    Use kmean algorithm (numpy version) to classify dataset provided.

    Parameters
    ----------
    filename : Path
        A given Path, such as "samples.csv"

    clusters : int, optional
        Number of clusters to divide the dataset into, default is 3

    iterations : int, optional
        Number of iterations to upload the centres, default is 10

    Returns
    -------
    alloc : np.ndarray
        Index of clusters where each point belong to
    """
    # This function is from clustering_numpy.
    data = load_data(filename)
    # Perform the algorithm to the dataset we loaded.
    alloc, centres = cluster(data, clusters, iterations)

    return alloc
