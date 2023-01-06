from math import *
from random import *
from pathlib import Path
import csv
from argparse import ArgumentParser


def load_data(filepath: Path):
    points = []
    with open(filepath) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            current = tuple(map(float, row))
            points.append(current)
    return points


def distance(point1: tuple, point2: tuple):
    dist = sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)
    return dist


def cluster(data: list, iterations: int):
    num = len(data)
    centres = [data[randrange(num)], data[randrange(num)], data[randrange(num)]]
    alloc = [None] * num
    count = 0
    while count < iterations:
        for i in range(num):
            point = data[i]
            dist = [None] * 3
            dist[0] = distance(point, centres[0])
            dist[1] = distance(point, centres[1])
            dist[2] = distance(point, centres[2])
            alloc[i] = dist.index(min(dist))
        for i in range(3):
            alloc_ps = [p for j, p in enumerate(data) if alloc[j] == i]
            new_mean = (sum([a[0] for a in alloc_ps]) / len(alloc_ps),
                        sum([a[1] for a in alloc_ps]) / len(alloc_ps), sum([a[2] for a in alloc_ps]) / len(alloc_ps))
            centres[i] = new_mean
        count = count + 1

    return alloc, centres


def process():
    parser = ArgumentParser(description="Generate clusters using kmean")
    parser.add_argument('--iters', type=int, default=10)
    parser.add_argument('Path')
    arguments = parser.parse_args()
    data = load_data(Path(f'{arguments.Path}'))
    alloc, centres = cluster(data, arguments.iters)
    for i in range(3):
        alloc_ps = [p for j, p in enumerate(data) if alloc[j] == i]
        print("Cluster " + str(i) + " is centred at " + str(centres[i]) +
              " and has " + str(len(alloc_ps)) + " points.")
        print(alloc_ps)


if __name__ == "__main__":
    process()
