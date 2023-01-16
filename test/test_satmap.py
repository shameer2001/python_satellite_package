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

    


