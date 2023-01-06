from math import *
from random import *
from pathlib import Path
import csv


def load_data(filepath: Path):
    points = []
    with open(filepath) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            current = tuple(map(float, row))
            points.append(current)
    return points


points = load_data(Path("samples.csv"))

centres = [points[randrange(len(points))], points[randrange(len(points))], points[randrange(len(points))]]

alloc = [None] * len(points)
count = 0
while count < 10:
    for i in range(len(points)):
        point = points[i]
        dist = [None] * 3
        dist[0] = sqrt((point[0] - centres[0][0]) ** 2 + (point[1] - centres[0][1]) ** 2 + (point[2] - centres[0][2]) ** 2)
        dist[1] = sqrt((point[0] - centres[1][0]) ** 2 + (point[1] - centres[1][1]) ** 2 + (point[2] - centres[1][2]) ** 2)
        dist[2] = sqrt((point[0] - centres[2][0]) ** 2 + (point[1] - centres[2][1]) ** 2 + (point[2] - centres[2][2]) ** 2)
        alloc[i] = dist.index(min(dist))
    for i in range(3):
        alloc_ps = [p for j, p in enumerate(points) if alloc[j] == i]
        new_mean = (sum([a[0] for a in alloc_ps]) / len(alloc_ps), sum([a[1] for a in alloc_ps]) / len(alloc_ps),
                    sum([a[2] for a in alloc_ps]) / len(alloc_ps))
        centres[i] = new_mean
    count = count + 1

for i in range(3):
    alloc_ps = [p for j, p in enumerate(points) if alloc[j] == i]
    print("Cluster " + str(i) + " is centred at " + str(centres[i]) + " and has " + str(len(alloc_ps)) + " points.")

    print(alloc_ps)
