from clustering_numpy import *
from pathlib import Path


def kmeans(filename: Path, clusters: int = 3, iterations: int = 10):
    data = load_data(filename)
    alloc, centres = cluster(data, clusters, iterations)

    return alloc
