from clustering_numpy import *
from pathlib import Path
from typing import Union


# Add a function kmeans() to perform kmean algorithm on csv file provided.
def kmeans(filename: Union[Path, str], clusters: int = 3, iterations: int = 10):
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
    # error raising: filename using wrong format
    if not (isinstance(filename, Path) or isinstance(filename, str)):
        raise TypeError("The filename must be a Path or string")

    # error raising: clusters using wrong format
    if not isinstance(clusters, int):
        raise TypeError("Clusters must be an integer")

    # error raising: iterations using wrong format
    if not isinstance(iterations, int):
        raise TypeError("iterations must be an integer")

    # This function is from clustering_numpy.
    data = load_data(filename)
    # Perform the algorithm to the dataset we loaded.
    alloc, centres = cluster(data, clusters, iterations)

    return alloc


print(kmeans("samples.csv", 4))
