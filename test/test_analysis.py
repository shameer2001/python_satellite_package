import numpy as np
from pytest import raises
from aigeanpy.analysis import kmeans


# Negative test
def test_kmeans_fails_on_wrong_format_filename():
    """Add negative test for kmean() which fails on wrong format of filename.
    """
    with raises(TypeError, match="The filename must be a Path or string"):
        kmeans(6.32)


def test_kmeans_fails_on_non_csv_file():
    """Add negative test for kmean() which fails on non csv inputted file.
    """
    with raises(TypeError, match="The file inputted must be a csv file"):
        kmeans("../samples.txt")


def test_kmeans_fails_on_non_integer_clusters():
    """Add negative test for kmean() which fails on non integer clusters.
    """
    with raises(TypeError, match="Clusters must be an integer"):
        kmeans("../samples.csv", 3.6)


def test_kmeans_fails_on_non_integer_iterations():
    """Add negative test for kmean() which fails on non integer iterations.
    """
    with raises(TypeError, match="iterations must be an integer"):
        kmeans("../samples.csv", 3, 14.3)


def test_kmeans_fails_on_non_positive_clusters_and_iterations():
    """Add negative test for kmean() which fails on non-positive clusters or iterations.
    """
    with raises(TypeError, match="clusters and iterations must be positive"):
        kmeans("../samples.csv", -3, 14)
    with raises(TypeError, match="clusters and iterations must be positive"):
        kmeans("../samples.csv", 3, -14)
    with raises(TypeError, match="clusters and iterations must be positive"):
        kmeans("../samples.csv", -3, -14)


# Unit test for kmeans
def test_kmeans():
    """Add a unit test for function kmeans() to determine whether this algorithm divides the dataset into
    default clusters.
    """
    index = kmeans("../samples.csv")
    assert len(index) == 3
