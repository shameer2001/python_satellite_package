import numpy as np
from math import *
from random import *
from pathlib import Path
import csv
from argparse import ArgumentParser


def load_data(filepath: Path):
    data = np.loadtxt(filepath, dtype=float, delimiter=',')
    return data


def distance(point1: tuple, point2: tuple):
    dist = sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)
    return dist


def cluster(data: list, clusters: int = 3, iterations: int = 10):
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


def process():
    parser = ArgumentParser(description="Generate clusters using kmean")
    parser.add_argument('--iters', type=int, default=10)
    parser.add_argument('--clusters', type=int, default=3)
    parser.add_argument('Path')
    arguments = parser.parse_args()
    data = load_data(Path(f'{arguments.Path}'))
    alloc, centres = cluster(data, arguments.clusters, arguments.iters)
    k = len(centres)
    for i in range(k):
        alloc_ps = [p for j, p in enumerate(data) if alloc[j] == i]
        print("Cluster " + str(i) + " is centred at " + str(centres[i]) +
              " and has " + str(len(alloc_ps)) + " points.")
        print(alloc_ps)


if __name__ == "__main__":
    process()
