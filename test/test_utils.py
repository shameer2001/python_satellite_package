
from aigeanpy.utils import *
import numpy as np
import pytest
from pytest import approx

############################## Conversion between pixel and earth coord ###################################


@pytest.mark.parametrize('pixel_coord, meta, resolution, expect_earth_coord', [
    # the case that single pixel maps to multiple earth coords, and the resolution is provided by the meta
    {'pixel_coord': np.array([[3, 2, 1], [4, 5, 6], [7, 8, 9]]),
     'meta': {'archive': 'ISA', 'year': 2023, 'observatory': 'Aigean', 'instrument': 'Fand', 'date': '2022-12-05',
              'time': '19:22:10', 'xcoords': [300.0, 309.0], 'ycoords': [50.0, 59.0], 'resolution': 3},
     'resolution': None,
     'expect_earth_coord': np.array(
         [[3, 3, 3, 2, 2, 2, 1, 1, 1], [3, 3, 3, 2, 2, 2, 1, 1, 1], [3, 3, 3, 2, 2, 2, 1, 1, 1],
          [4, 4, 4, 5, 5, 5, 6, 6, 6], [4, 4, 4, 5, 5, 5, 6, 6, 6], [4, 4, 4, 5, 5, 5, 6, 6, 6],
          [7, 7, 7, 8, 8, 8, 9, 9, 9], [7, 7, 7, 8, 8, 8, 9, 9, 9], [7, 7, 7, 8, 8, 8, 9, 9, 9]])},

    # the case that single pixel maps to multiple earth coords, and the resolution is provided explicitly
    {'pixel_coord': np.array([[3, 2, 1], [4, 5, 6], [7, 8, 9]]),
     'meta': {'archive': 'ISA', 'year': 2023, 'observatory': 'Aigean', 'instrument': 'Fand', 'date': '2022-12-05',
              'time': '19:22:10', 'xcoords': [300.0, 306.0], 'ycoords': [50.0, 56.0], 'resolution': 2},
     'resolution': 3,
     'expect_earth_coord': np.array(
         [[3, 3, 3, 2, 2, 2, 1, 1, 1], [3, 3, 3, 2, 2, 2, 1, 1, 1], [3, 3, 3, 2, 2, 2, 1, 1, 1],
          [4, 4, 4, 5, 5, 5, 6, 6, 6], [4, 4, 4, 5, 5, 5, 6, 6, 6], [4, 4, 4, 5, 5, 5, 6, 6, 6],
          [7, 7, 7, 8, 8, 8, 9, 9, 9], [7, 7, 7, 8, 8, 8, 9, 9, 9], [7, 7, 7, 8, 8, 8, 9, 9, 9]])},

    # the case that multiple pixel maps to single earth coords, and the resolution is provided by the meta
    {'pixel_coord': np.array([[2, 3, 3, 4, 6, 7, 8, 9], [3, 4, 7, 8, 9, 10, 11, 12], [9, 9, 8, 7, 7, 6, 10, 11],
                              [14, 50, 40, 70, 9, 8, 1, 2], [9, 8, 7, 6, 5, 4, 3, 2], [4, 4, 3, 2, 1, 1, 2, 3]]),
     'meta': {'archive': 'ISA', 'year': 2023, 'observatory': 'Aigean', 'instrument': 'Fand', 'date': '2022-12-05',
              'time': '19:22:10', 'xcoords': [300.0, 302.7], 'ycoords': [50.0, 52.0], 'resolution': 1/3},
     'resolution': None,
     'expect_earth_coord': np.array([[2, 4, 8], [14, 70, 1]])},

    # the case that multiple pixel maps to single earth coords, and the resolution is provided explicitly
    {'pixel_coord': np.array([[2, 3, 3, 4, 6, 7, 8, 9], [3, 4, 7, 8, 9, 10, 11, 12], [9, 9, 8, 7, 7, 6, 10, 11],
                              [14, 50, 40, 70, 9, 8, 1, 2], [9, 8, 7, 6, 5, 4, 3, 2], [4, 4, 3, 2, 1, 1, 2, 3]]),
     'meta': {'archive': 'ISA', 'year': 2023, 'observatory': 'Aigean', 'instrument': 'Fand', 'date': '2022-12-05',
              'time': '19:22:10', 'xcoords': [300.0, 306.0], 'ycoords': [50.0, 56.0], 'resolution': 2},
     'resolution': 1/3,
     'expect_earth_coord': np.array([[2, 4, 8], [14, 70, 1]])}
])
def test_pixel_to_earth(pixel_coord, meta, resolution, expect_earth_coord):
    """Testing the pixel_to_earth() function for converting the image under pixel coord to the image under earth coord.
    """
    ...


@pytest.mark.parametrize('earth_coord, meta, resolution, expect_pixel_coord', [
    # the case that single pixel maps to multiple earth coords, and the resolution is provided by the meta
    {'earth_coord': np.array(
         [[3, 3, 3, 2, 2, 2, 1, 1, 1], [3, 3, 3, 2, 2, 2, 1, 1, 1], [3, 3, 3, 2, 2, 2, 1, 1, 1],
          [4, 4, 4, 5, 5, 5, 6, 6, 6], [4, 4, 4, 5, 5, 5, 6, 6, 6], [4, 4, 4, 5, 5, 5, 6, 6, 6],
          [7, 7, 7, 9, 9, 9, 10, 10, 10], [7, 7, 7, 9, 9, 9, 10, 10, 10], [7, 7, 7, 9, 9, 9, 10, 10, 10]]),
     'meta': {'archive': 'ISA', 'year': 2023, 'observatory': 'Aigean', 'instrument': 'Fand', 'date': '2022-12-05',
              'time': '19:22:10', 'xcoords': [300.0, 309.0], 'ycoords': [50.0, 59.0], 'resolution': 3},
     'resolution': None,
     'expected_pixel_coord': np.array([[3, 2, 1], [4, 5, 6], [7, 9, 10]])},

    # the case that single pixel maps to multiple earth coords, and the resolution is provided explicitly
    {'earth_coord': np.array(
         [[3, 3, 3, 2, 2, 2, 1, 1, 1], [3, 3, 3, 2, 2, 2, 1, 1, 1], [3, 3, 3, 2, 2, 2, 1, 1, 1],
          [4, 4, 4, 5, 5, 5, 6, 6, 6], [4, 4, 4, 5, 5, 5, 6, 6, 6], [4, 4, 4, 5, 5, 5, 6, 6, 6],
          [7, 7, 7, 9, 9, 9, 10, 10, 10], [7, 7, 7, 9, 9, 9, 10, 10, 10], [7, 7, 7, 9, 9, 9, 10, 10, 10]]),
     'meta': {'archive': 'ISA', 'year': 2023, 'observatory': 'Aigean', 'instrument': 'Fand', 'date': '2022-12-05',
              'time': '19:22:10', 'xcoords': [300.0, 306.0], 'ycoords': [50.0, 56.0], 'resolution': 2},
     'resolution': 3,
     'expected_pixel_coord': np.array([[3, 2, 1], [4, 5, 6], [7, 9, 10]])},

    # the case that multiple pixel maps to single earth coords, and the resolution is provided by the meta
    {'earth_coord': np.array([[2, 4, 8], [14, 70, 1]]),
     'meta': {'archive': 'ISA', 'year': 2023, 'observatory': 'Aigean', 'instrument': 'Fand', 'date': '2022-12-05',
              'time': '19:22:10', 'xcoords': [300.0, 302.7], 'ycoords': [50.0, 52.0], 'resolution': 1/3},
     'resolution': None,
     'expected_pixel_coord': np.array([[2, 2, 2, 4, 4, 4, 8, 8], [2, 2, 2, 4, 4, 4, 8, 8], [2, 2, 2, 4, 4, 4, 8, 8],
                              [14, 14, 14, 70, 70, 70, 1, 1], [14, 14, 14, 70, 70, 70, 1, 1], [14, 14, 14, 70, 70, 70, 1, 1]])},

    # the case that multiple pixel maps to single earth coords, and the resolution is provided explicitly
    {'earth_coord': np.array([[2, 4, 8], [14, 70, 1]]),
     'meta': {'archive': 'ISA', 'year': 2023, 'observatory': 'Aigean', 'instrument': 'Fand', 'date': '2022-12-05',
              'time': '19:22:10', 'xcoords': [300.0, 306.0], 'ycoords': [50.0, 56.0], 'resolution': 2},
     'resolution': 1/3,
     'expected_pixel_coord': np.array([[2, 2, 2, 4, 4, 4, 8, 8], [2, 2, 2, 4, 4, 4, 8, 8], [2, 2, 2, 4, 4, 4, 8, 8],
                              [14, 14, 14, 70, 70, 70, 1, 1], [14, 14, 14, 70, 70, 70, 1, 1], [14, 14, 14, 70, 70, 70, 1, 1]])}
])
def test_earth_to_pixel(earth_coord, meta, resolution, expect_pixel_coord):
    """Testing the earth_to_pixel() function for converting the image under earth coord to the image under pixel coord.
    """
    ...
