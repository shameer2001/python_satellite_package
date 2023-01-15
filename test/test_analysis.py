from pytest import raises
from analysis import kmeans


# Negative test
def test_kmeans_fails_on_wrong_format_filename():
    with raises(TypeError, match="The filename must be a Path or string"):
        kmeans(6.32)


def test_kmeans_fails_on_non_csv_file():
    with raises(TypeError, match="The file inputted must be a csv file"):
        kmeans("samples.txt")


def test_kmeans_fails_on_non_integer_clusters():
    with raises(TypeError, match="Clusters must be an integer"):
        kmeans("samples.csv", 3.6)


def test_kmeans_fails_on_non_integer_iterations():
    with raises(TypeError, match="iterations must be an integer"):
        kmeans("samples.csv", 3, 14.3)


def test_kmeans_fails_on_non_positive_clusters_and_iterations():
    with raises(TypeError, match="clusters and iterations must be positive"):
        kmeans("samples.csv", -3, 14)
    with raises(TypeError, match="clusters and iterations must be positive"):
        kmeans("samples.csv", 3, -14)
    with raises(TypeError, match="clusters and iterations must be positive"):
        kmeans("samples.csv", -3, -14)
