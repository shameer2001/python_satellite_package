from pytest import raises
from analysis import kmeans


# Negative test
def test_kmeans_fails_on_wrong_format_filename():
    with raises(TypeError, match="The filename must be a Path or string"):
        kmeans(6.32)


