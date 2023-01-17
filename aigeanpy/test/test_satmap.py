from net import *
from satmap import *
import pytest
from pytest import approx

############################## SatMap attributes ###################################


@pytest.mark.parametrize('instruments', [('lir'), ('manannan'), ('fand')])
def test_meta_keys(instruments):
    '''Testing the meta-data output for correct key names.

    Parameters
    ----------
    instruments: str
                 The name of each instrument. Used to input all instruments one after the other automatically.
    '''

    query = net.query_isa("2022-12-18", "2022-12-21", instruments)
    net.download_isa(query[0]['filename'])
    satmap = get_satmap(query[0]['filename'])

    result = list(satmap.meta.keys()) # keys of the meta-data as a list


    if instruments=='lir': 
        expected_keys = ['asdf_library', 'history', 'archive', 'date', 'instrument', 'observatory', 'resolution', 'time', 'xcoords', 'ycoords', 'year']
    elif instruments=='manannan':
        expected_keys = ['archive', 'year', 'date', 'instrument', 'observatory', 'resolution', 'time', 'xcoords', 'ycoords']     
    elif instruments=='fand':
        expected_keys = ['archive', 'year', 'observatory', 'instrument', 'date', 'time', 'xcoords', 'ycoords', 'resolution']


    assert result == expected_keys, "One or more of the keys in the meta-data is incorrect."



# input the instrument name when inputting into query service with the corresponding capitalised name in the meta data:
@pytest.mark.parametrize('instruments, instrument_name', [('lir', 'Lir'), ('manannan', 'Manannan'), ('fand', 'Fand')]) 
def test_meta_instr(instruments, instrument_name):
    '''Testing the instrument name in the meta-data.
    '''
    query = net.query_isa("2023-01-07", "2023-01-10", instruments)
    net.download_isa(query[0]['filename'])
    satmap = get_satmap(query[0]['filename'])

    result = satmap.meta['instrument'] # keys of the meta-data as a list
    expected_instr = instrument_name


    assert result == expected_instr, "The instrument in the meta=data does not match the input." 



# input the instrument name with the corresponding expected resolutions one after the other:
@pytest.mark.parametrize('instruments, resolutions', [('lir', 30), ('manannan', 15), ('fand', 5)]) 
def test_meta_res(instruments, resolutions):
    '''Testing that the resolution in the meta-data is as expected.
    '''
    query = net.query_isa("2023-01-10", "2023-01-13", instruments)
    net.download_isa(query[0]['filename'])
    satmap = get_satmap(query[0]['filename'])

    result = satmap.meta['resolution'] 
    expected_res = resolutions


    assert result == expected_res, "The resolution does not match expected resolution of the corresponding instrument."
    


# input the instrument name with the corresponding expected shapes one after the other:
@pytest.mark.parametrize('instruments, shapes', [('lir', (10,20)), ('manannan', (10,30)), ('fand', (10,45))]) 
def test_data_shape(instruments, shapes):

    query = net.query_isa("2023-01-01", "2023-01-04", instruments)
    net.download_isa(query[0]['filename'])
    satmap = get_satmap(query[0]['filename'])

    result = satmap.shape
    expected_res = shapes


    assert result == expected_res, "The data-shape does not match the expected data-shape from the corresponding instrument."

    


# input the instrument name with the corresponding expected "field of views" one after the other:
@pytest.mark.parametrize('instruments, FOVs', [('lir', (600,300) ), ('manannan', (450,150) ), ('fand', (225,50) )]) # expected fov calculated with excel
def test_data_fov(instruments, FOVs):
    '''Testing that the field of view is correct with the expected result form excel
    '''
    query = net.query_isa("2022-12-15", "2022-12-17", instruments)
    net.download_isa(query[0]['filename'])
    satmap = get_satmap(query[0]['filename'])

    result = satmap.fov
    expected_fov = FOVs


    assert result == approx(expected_fov, rel=0.1), "The 'field of view' calculation is incorrect."



# input the instrument name with the corresponding expected "centres" one after the other:
@pytest.mark.parametrize('instruments, centres', [('lir', (300,150) ), ('manannan', (225, 75) ), ('fand', (187.5,25) )]) # expected centre calculated with excel
def test_data_centre(instruments, centres):

    query = net.query_isa("2022-12-02", "2022-12-05", instruments)
    net.download_isa(query[0]['filename'])
    satmap = get_satmap(query[0]['filename'])

    result = satmap.centre
    expected_centre = centres


    assert result == approx(expected_centre, rel=0.1), "The calculation of the centre of the image is incorrect."






 






########## NEGATIVE TESTS ###########



def test_get_satmap_typeerror():
    '''Test case where file_name input is not a string
    '''
    with pytest.raises(TypeError, match="The file-name must be a string"):
        get_satmap(123)

def test_get_satmap_filenotfounderror():
    '''Test case where file does not exist
    '''
    with pytest.raises(FileNotFoundError, match="The input file does not exist."):
        get_satmap("non_existent_file.asdf")

def test_get_satmap_nameerror():
    '''Test case where file format is not supported
    '''
    with pytest.raises(NameError, match="The file format is not supported. Only these are accepted: ASDF, HDF5 and ZIP."):
        get_satmap("file.txt")  