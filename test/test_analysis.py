from pytest import raises
from analysis import kmeans


# Negative test
def test_kmeans_fails_on_wrong_format_filename():
    with raises(TypeError, match="The filename must be a Path or string"):
        kmeans(6.32)


def test_kmeans_fails_on_non_csv_file():
    with raises(TypeError, match="The file inputted must be a csv file"):
        kmeans("samples.txt")
