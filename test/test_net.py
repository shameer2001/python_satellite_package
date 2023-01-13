from net import *
import pytest
import numpy as np


# Use pytest to create a parameter that will insert all instruments one-by-one :
@pytest.mark.parametrize('instruments',
[
    ('lir'),
    ('manannan'),
    ('fand'),
    ('ecne'),
]
)


def test_query_isa(instruments):
    '''Testing the query_isa() function from the `net` class.

    Parameters
    ----------

    instruments: str
                 The name of each instrument. Used to input all instruments one after the other automatically.
    
    '''


    # Test with normal dates and for all instruments:

    query = net.query_isa("2022-12-05", "2022-12-07", instruments)
    expected_query_keys = ['date', 'filename', 'instrument', 'resolution', 'time', 'xcoords',  'ycoords']
    
    for i in query: assert list( i.keys() ) == expected_query_keys # test for key names
    for i in query: assert i['instrument'] == instruments # test for instrument type
    for i in query: assert (np.size(i['xcoords']) == 2 and np.size(i['ycoords']) == 2)  # test for shape of x and y coordinate range
    assert query[0]['date'] == "2022-12-05" # test for start date
    assert query[-1]['date'] == "2022-12-07" # test for end date
    


    # Test for default dates and instrument:

    query = net.query_isa()  
    todays_date = str( dt.today().strftime('%Y-%m-%d') ) # todays date using `datetime`


    for i in query: assert list( i.keys() ) == expected_query_keys
    for i in query: assert (i['instrument']=='lir' or i['instrument']=='manannan' or i['instrument']=='fand' or i['instrument']=='ecne')
    for i in query: assert (np.size(i['xcoords']) == 2 and np.size(i['ycoords']) == 2)
    assert query[0]['date'] == todays_date
    assert query[-1]['date'] == todays_date