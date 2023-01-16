
from aigeanpy.satmap import *
import pytest
from pytest import approx

############################## SatMap methods ###################################


# input the instrument name with the corresponding expected shapes one after the other:
@pytest.mark.parametrize('date, xcoords, ycoords, shape, commonX, commonY, AX, AY', [
    ("2023-01-03", [200.0, 1100.0], [0.0, 300.0], (10, 30), [10, 20], [0, 10], [10, 20], [0, 10])
])
def test_add(date, xcoords, ycoords, shape, commonX, commonY, AX, AY):
    """Testing the SatMap.__add__() function for adding two images taken in the same day and using the same instrument
    """
    query = net.query_isa(date, date, 'lir')
    net.download_isa(query[0]['filename'])
    net.download_isa(query[1]['filename'])

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


#@pytest.mark.parametrize('start, stop, xcoords, ycoords, shape, AX, AY, BX, BY', [
#    ("2023-01-03", "2023-01-04", [600.0, 800.0], [0.0, 300.0], (10, 7), [14, 27], [0, 10], [0, 7], [0, 10])
#])
#def test_sub(start, stop, xcoords, ycoords, shape, AX, AY, BX, BY):
    """Testing the SatMap.__sub__() function for subtracting two images taken in the different days and using the same instrument
    """
    """

    query = net.query_isa(start, stop, 'lir')
    net.download_isa(query[0]['filename'])
    net.download_isa(query[-1]['filename'])

    satmapA = get_satmap(query[0]['filename'])
    satmapB = get_satmap(query[-1]['filename'])

    satmap = satmapA - satmapB

    assert satmap.meta['xcoords'] == xcoords
    assert satmap.meta['ycoords'] == ycoords
    assert satmap.meta['extra'] == 'subtract'
    assert satmap.shape == approx(shape, rel=0.1)

    # x, y for the satmapA (overlap)
    AXLow, AXHigh = AX
    AYLow, AYHigh = AY

    # x, y for the satmapB (overlap)
    BXLow, BXHigh = BX
    BYLow, BYHigh = BY

    assert satmap.data == satmapA.data[AYLow:AYHigh, AXLow:AXHigh] - satmapB.data[BYLow:BYHigh, BXLow:BXHigh]
        """



#@pytest.mark.parametrize('date, instruments, xcoords, ycoords, shape, commonX, commonY, AX, AY, resolution, padding', [
#    ("2023-01-03", ['lir', 'manannan'], [0.0, 800.0], [0.0, 300.0], (10, 7), [14, 27], [0, 10], [0, 7], [0, 10])
#])
#def test_mosaic(date, instruments, xcoords, ycoords, shape, commonX, commonY, AX, AY, resolution, padding):
    """#Testing the SatMap.mosaic() function for adding two images taken in the same day, but it can use different instruments
"""
"""
    queryA = net.query_isa(date, date, instruments[0])
    net.download_isa(queryA[0]['filename'])

    queryB = net.query_isa(date, date, instruments[1])
    net.download_isa(queryB[0]['filename'])

    satmapA = get_satmap(queryA[0]['filename'])
    satmapB = get_satmap(queryB[0]['filename'])

    satmap = satmapA.mosaic(satmapB, resolution, padding)

    assert satmap.meta['xcoords'] == xcoords
    assert satmap.meta['ycoords'] == ycoords
    assert satmap.meta['extra'] == 'mosaic'
    assert satmap.shape == approx(shape, rel=0.1)

    # x, y for the combined image (overlap)
    commonXLow, commonXHigh = commonX
    commonYLow, commonYHigh = commonY

    # x, y for the satmapA (overlap)
    AXLow, AXHigh = AX
    AYLow, AYHigh = AY

    assert satmap.data[commonYLow:commonYHigh, commonXLow:commonXHigh] == satmapA.data[AYLow:AYHigh, AXLow:AXHigh]
    """

if __name__ == '__main__':
   pytest.main(["-s","-v","test_satmap_method.py"])