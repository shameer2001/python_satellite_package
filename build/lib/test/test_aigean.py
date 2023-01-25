import pytest
from pathlib import Path
from aigeanpy.aigean_today import aigean_today
from aigeanpy.aigean_metadata import aigean_metadata
from aigeanpy.aigean_mosaic import aigean_mosaic


# TESTS FOR COMMAND-LINE FUNCTIONS #

######### aigean_today NEGATIVE TESTS ##########

def test_instrument_input_type_error():
    with pytest.raises(TypeError) as exception:
        aigean_today(123)
    assert str(exception.value) == "Name of instrument input must be string."

def test_instrument_input_value_error():
    with pytest.raises(ValueError) as exception:
        aigean_today('abc')
    assert str(exception.value) == "Name of instrument input is not available. The only available instruments are: 'lir', 'manannan', 'fand' or 'ecne'."


######### aigean_metadata NEGATIVE TESTS ##########

def test_filename_input_type_error():
    with pytest.raises(TypeError) as exception:
        aigean_metadata([123, 251.23])
    assert str(exception.value) == "Name of files input must be string."


def test_filename_input_name_error():
    with pytest.raises(NameError) as exception:
        aigean_metadata(['abc'])
    assert str(exception.value) == "The file format is not supported. Only these are accepted: ASDF, HDF5 and ZIP."


def test_filename_input_name_error_str():
    with pytest.raises(NameError) as exception:
        aigean_metadata('abc')
    assert str(exception.value) == "The file format is not supported. Only these are accepted: ASDF, HDF5 and ZIP."






######### aigean_metadata POSITIVE TESTS ##########


def test_function_return_archive():
    # use 'aigean_man_20221205_194510.hdf5' as test sample

    output = aigean_metadata(['aigean_man_20221205_194510.hdf5'])

    assert output['archive:'] == 'ISA', "Archive name output is wrong"

def test_function_return_observatory():
    output = aigean_metadata(['aigean_man_20221205_194510.hdf5'])

    assert output['observatory:'] == 'Aigean', "Observatory name output is wrong"

def test_function_return_instrument():
    output = aigean_metadata(['aigean_man_20221205_194510.hdf5'])

    assert output['instrument:'] == 'Manannan', "Instrument name is wrong"

def test_function_return_obsdate():
    output = aigean_metadata(['aigean_man_20221205_194510.hdf5'])
    assert output['obs_date:'] == '2022-12-05 19:45:10', "Observation's date and time is wrong"






######### aigean_mosaic NEGATIVE TEST ##########


def test_input_value_error():
# use 'aigean_man_20221205_194510.hdf5' as test sample
    with pytest.raises(ValueError) as exception:
        aigean_mosaic(['aigean_man_20221205_194510.hdf5'])
    assert str(exception.value) == "Only two or more filename inputs are acceptable."