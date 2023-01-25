
from aigeanpy.satmap import *
import pytest
from pytest import approx

############################## SatMap methods ###################################



@pytest.mark.parametrize('date, xcoords, ycoords, shape, commonX, commonY, AX, AY', [
    ("2023-01-03", [200.0, 1100.0], [0.0, 300.0], (10, 30), [10, 20], [0, 10], [10, 20], [0, 10])
])
def test_add(date, xcoords, ycoords, shape, commonX, commonY, AX, AY):
    """Testing the SatMap.__add__() function for adding two images taken in the same day and using the same instrument
    """
    query = query_isa(date, date, 'lir')
    download_isa(query[0]['filename'])
    download_isa(query[1]['filename'])

    satmapA = get_satmap(query[0]['filename'])
    satmapB = get_satmap(query[1]['filename'])

    satmap = satmapA + satmapB

    assert satmap.meta['xcoords'] == xcoords
    assert satmap.meta['ycoords'] == ycoords
    assert satmap.meta['source'] == 'add'
    assert satmap.shape == approx(shape, rel=0.1)

    # x, y for the combined image (overlap)
    commonXLow, commonXHigh = commonX
    commonYLow, commonYHigh = commonY

    # x, y for the satmapA (overlap)
    AXLow, AXHigh = AX
    AYLow, AYHigh = AY

    assert satmap.data[commonYLow:commonYHigh, commonXLow:commonXHigh].all() == satmapA.data[AYLow:AYHigh, AXLow:AXHigh].all()


@pytest.mark.parametrize('start, stop, xcoords, ycoords, shape, AX, AY, BX, BY', [
    ("2023-01-07", "2023-01-10", [400.0, 700.0], [200.0, 500.0], (10, 10), [10, 20], [0, 10], [0, 10], [0, 10])
])
def test_sub(start, stop, xcoords, ycoords, shape, AX, AY, BX, BY):
    """Testing the SatMap.__sub__() function for subtracting two images taken in the different days and using the same instrument
    """


    query = query_isa(start, stop, 'lir')
    download_isa(query[0]['filename'])
    download_isa(query[-1]['filename'])

    satmapA = get_satmap(query[0]['filename'])
    satmapB = get_satmap(query[-1]['filename'])

    satmap = satmapA - satmapB

    assert satmap.meta['xcoords'] == xcoords
    assert satmap.meta['ycoords'] == ycoords
    assert satmap.meta['source'] == 'subtract'
    assert satmap.shape == approx(shape, rel=0.1)

    # x, y for the satmapA (overlap)
    AXLow, AXHigh = AX
    AYLow, AYHigh = AY

    # x, y for the satmapB (overlap)
    BXLow, BXHigh = BX
    BYLow, BYHigh = BY

    assert satmap.data.all() == (satmapA.data[AYLow:AYHigh, AXLow:AXHigh] - satmapB.data[BYLow:BYHigh, BXLow:BXHigh]).all()



# @pytest.mark.parametrize('date, instruments, xcoords, ycoords, resolution, padding', [
#     ("2022-12-05", ['lir', 'manannan'], [0.0, 800.0], [0.0, 300.0], None, True),
#     ("2022-12-05", ['lir', 'manannan'], [0.0, 800.0], [0.0, 300.0], 20, True),
#     ("2022-12-05", ['lir', 'manannan'], [200.0, 450.0], [0.0, 150.0], None, False)
# ])
# def test_mosaic(date, instruments, xcoords, ycoords, resolution, padding):
#     """#Testing the SatMap.mosaic() function for adding two images taken in the same day, but it can use different instruments
# """

#     queryA = query_isa(date, date, instruments[0])
#     download_isa(queryA[0]['filename'])

#     queryB = query_isa(date, date, instruments[1])
#     download_isa(queryB[0]['filename'])

#     satmapA = get_satmap(queryA[0]['filename'])
#     satmapB = get_satmap(queryB[0]['filename'])

#     result1 = satmapA.mosaic(satmapB, resolution, padding)
#     result2 = satmapB.mosaic(satmapA, resolution, padding)

#     assert result1.meta['xcoords'] == result2.meta['xcoords'] == xcoords
#     assert result1.meta['ycoords'] == result2.meta['ycoords'] == ycoords
#     assert result1.meta['source'] == result2.meta['source'] == 'mosaic'
#     assert result1.shape == result2.shape
#     assert result1.data.all() == result2.data.all()



########## NEGATIVE TESTS ###########

@pytest.mark.parametrize('date, instruments', [
    ("2022-12-15", ['lir', 'manannan'])
])
def test_add_with_different_resolution(date, instruments):
    """Testing the SatMap.__add__() function for adding two images taken in the same day and using different instruments
    """
    queryA = query_isa(date, date, instruments[0])
    download_isa(queryA[0]['filename'])

    queryB = query_isa(date, date, instruments[1])
    download_isa(queryB[0]['filename'])

    satmapA = get_satmap(queryA[0]['filename'])
    satmapB = get_satmap(queryB[0]['filename'])

    with pytest.raises(TypeError, match="only the images from the same instrument can be added"):
        satmapA + satmapB


@pytest.mark.parametrize('date, instruments', [
    (["2022-12-20", "2022-12-22"], 'lir')
])
def test_add_from_different_date(date, instruments):
    """Testing the SatMap.__add__() function for adding two images taken in the same day and using different instruments
    """
    query = query_isa(date[0], date[1], instruments)
    download_isa(query[0]['filename'])
    download_isa(query[-1]['filename'])

    satmapA = get_satmap(query[0]['filename'])
    satmapB = get_satmap(query[-1]['filename'])

    with pytest.raises(TypeError, match="only the images from the same day can be added"):
        satmapA + satmapB


@pytest.mark.parametrize('date, instrument', [
    ("2022-12-05", 'lir')
])
def test_sub_from_same_date(date, instrument):
    """Testing the SatMap.__add__() function for adding two images taken in the same day and using different instruments
    """
    query = query_isa(date, date, instrument)
    download_isa(query[0]['filename'])
    download_isa(query[1]['filename'])

    satmapA = get_satmap(query[0]['filename'])
    satmapB = get_satmap(query[1]['filename'])

    with pytest.raises(TypeError, match="only the images from two different days can be subtracted"):
        satmapA - satmapB


@pytest.mark.parametrize('date, instrument', [
    (["2023-01-04", "2023-01-05"], "lir")
])
def test_sub_without_overlap(date, instrument):
    """Testing the SatMap.__add__() function for adding two images taken in the same day and using different instruments
    """
    query = query_isa(date[0], date[1], instrument)
    download_isa(query[0]['filename'])
    download_isa(query[-1]['filename'])

    satmapA = get_satmap(query[0]['filename'])
    satmapB = get_satmap(query[-1]['filename'])

    with pytest.raises(TypeError, match="two images can not be subtracted because they have no overlap"):
        satmapA - satmapB



if __name__ == '__main__':
   pytest.main(["-s", "-v", "test_satmap_method.py"])