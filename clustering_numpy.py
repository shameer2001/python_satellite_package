import numpy as np
from pathlib import Path
from argparse import ArgumentParser


def load_data(filepath: Path):
    data = np.loadtxt(filepath, dtype=float, delimiter=',')
    return data


def distance(centres: np.array, points: np.array):
    n, _ = np.shape(centres)
    m, _ = np.shape(points)
    mat_A = np.tile(np.matrix(np.square(points).sum(axis=1)).T, (1, n))
    mat_B = np.tile(np.matrix(np.square(centres).sum(axis=1)), (m, 1))
    mat_C = points @ centres.T
    mat_dist = np.sqrt(-2 * mat_C + mat_A + mat_B)
    return mat_dist


def cluster(data: np.array, clusters: int = 3, iterations: int = 10):
    num = len(data)
    k = clusters
    rand_index = np.random.randint(num, size=k)
    centres = data[rand_index]
    count = 0
    while count < iterations:
        dist_mat = distance(centres, data)
        alloc = np.array(np.argmin(dist_mat, axis=1).T)[0]
        for i in range(k):
            alloc_ps = np.array([p for j, p in enumerate(data) if alloc[j] == i])
            new_mean = np.array(np.sum(alloc_ps, axis=0) / len(alloc_ps))
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
        alloc_ps = [tuple(p) for j, p in enumerate(data) if alloc[j] == i]
        print("Cluster " + str(i) + " is centred at " + str(tuple(centres[i])) +
              " and has " + str(len(alloc_ps)) + " points.")
        print(alloc_ps)


if __name__ == "__main__":
    process()
