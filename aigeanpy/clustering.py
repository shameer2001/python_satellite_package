from math import *
from random import *
from pathlib import Path
import csv
from argparse import ArgumentParser


# Modify the way for loading data.
def load_data(filepath: Path):
    """
    Loading data from csv file.

    Parameters
    ----------
    filepath : Path
        A given Path, such as "samples.csv"

    Returns
    -------
    points : list
        The data (points) from the csv file.
    """
    points = []
    with open(filepath) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            current = tuple(map(float, row))
            points.append(current)
    return points


# Add this function to reduce repetition.
def distance(point1: tuple, point2: tuple):
    """
    Calculate the euclidean distance between two points.

    Parameters
    ----------
    point1 : tuple
        A given point, such as (5,5,3)

    point2 : tuple
        Another given point, such as (5,5,3)

    Returns
    -------
    dist : float
        Euclidean distance between two points
    """
    dist = sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)
    return dist


# Perform the kmean algorithm
def cluster(data: list, clusters: int = 3, iterations: int = 10):
    """
    Use kmean algorithm to classify dataset provided.

    Parameters
    ----------
    data : list
        Dataset loaded from the csv file, which is a list of tuples

    clusters : int, optional
        Number of clusters to divide the dataset into, default is 3

    iterations : int, optional
        Number of iterations to upload the centres, default is 10

    Returns
    -------
    alloc : list
        Index of clusters where each points belong to

    centres : list
        The final centres for each cluster
    """
    num = len(data)
    k = clusters
    centres = []
    for i in range(k):
        centres.append(data[randrange(num)])
    alloc = [None] * num
    count = 0
    while count < iterations:
        for i in range(num):
            point = data[i]
            dist = [None] * k
            # Use distance function to reduce repetition
            for j in range(k):
                dist[j] = distance(point, centres[j])
            alloc[i] = dist.index(min(dist))
        for i in range(k):
            alloc_ps = [p for j, p in enumerate(data) if alloc[j] == i]
            new_mean = (sum([a[0] for a in alloc_ps]) / len(alloc_ps),
                        sum([a[1] for a in alloc_ps]) / len(alloc_ps), sum([a[2] for a in alloc_ps]) / len(alloc_ps))
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
    data = load_data(arguments.Path)
    alloc, centres = cluster(data, arguments.clusters, arguments.iters)
    k = len(centres)
    # Print the final result.
    for i in range(k):
        alloc_ps = [p for j, p in enumerate(data) if alloc[j] == i]
        print("Cluster " + str(i) + " is centred at " + str(centres[i]) +
              " and has " + str(len(alloc_ps)) + " points.")
        print(alloc_ps)


if __name__ == "__main__":
    process()
