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


ps = load_data(Path("samples.csv"))

m = [ps[randrange(len(ps))], ps[randrange(len(ps))], ps[randrange(len(ps))]]

alloc = [None] * len(ps)
n = 0
while n < 10:
    for i in range(len(ps)):
        p = ps[i]
        d = [None] * 3
        d[0] = sqrt((p[0] - m[0][0]) ** 2 + (p[1] - m[0][1]) ** 2 + (p[2] - m[0][2]) ** 2)
        d[1] = sqrt((p[0] - m[1][0]) ** 2 + (p[1] - m[1][1]) ** 2 + (p[2] - m[1][2]) ** 2)
        d[2] = sqrt((p[0] - m[2][0]) ** 2 + (p[1] - m[2][1]) ** 2 + (p[2] - m[2][2]) ** 2)
        alloc[i] = d.index(min(d))
    for i in range(3):
        alloc_ps = [p for j, p in enumerate(ps) if alloc[j] == i]
        new_mean = (sum([a[0] for a in alloc_ps]) / len(alloc_ps), sum([a[1] for a in alloc_ps]) / len(alloc_ps),
                    sum([a[2] for a in alloc_ps]) / len(alloc_ps))
        m[i] = new_mean
    n = n + 1

for i in range(3):
    alloc_ps = [p for j, p in enumerate(ps) if alloc[j] == i]
    print("Cluster " + str(i) + " is centred at " + str(m[i]) + " and has " + str(len(alloc_ps)) + " points.")

    print(alloc_ps)
