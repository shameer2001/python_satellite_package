import pytest

from aigeanpy.satmap import *


############################## Conversion between pixel and earth coord ###################################


@pytest.mark.parametrize('date, instrument', [
    ("2023-01-04", 'lir'),
    ("2023-01-06", 'manannan')
])
def test_conversion(date, instrument):
    """Testing the pixel_to_earth() and earth_to_pixel() functions
    """
    query = query_isa(date, date, instrument)
    download_isa(query[0]['filename'])

    satmap = get_satmap(query[0]['filename'])

    estimated_earth = pixel_to_earth(satmap.data, satmap.meta)

    assert np.array(satmap.data).all() == earth_to_pixel(estimated_earth['earthCoord'], satmap.meta).all()
    assert len(estimated_earth['earthCoord']) == satmap.meta['ycoords'][1] - satmap.meta['ycoords'][0]
    assert len(estimated_earth['earthCoord'][0]) == satmap.meta['xcoords'][1] - satmap.meta['xcoords'][0]

if __name__ == '__main__':
   pytest.main(["-s", "-v", "test_utils.py"])