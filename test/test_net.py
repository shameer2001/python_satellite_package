from net import *
import pytest
import numpy as np


############################## query_isa():###################################

# Test with normal dates and for all instruments:

# Use pytest to create a parameter that will insert all instruments one-by-one :
@pytest.mark.parametrize('instruments',
[
    ('lir'),
    ('manannan'),
    ('fand'),
    ('ecne'),
]
)
def test_query_keys(instruments):
    '''Testing the query_isa() function for key names.

    Parameters
    ----------
    instruments: str
                 The name of each instrument. Used to input all instruments one after the other automatically.
    '''
    
    query = net.query_isa("2022-12-05", "2022-12-07", instruments)
    expected_query_keys = ['date', 'filename', 'instrument', 'resolution', 'time', 'xcoords',  'ycoords']

    # use for loop to test all dict in output:
    for i in query: assert list( i.keys() ) == expected_query_keys, "One or more of the keys in one or more of the query result(s) is incorrect."



@pytest.mark.parametrize('instruments', [('lir'), ('manannan'), ('fand'), ('ecne'),])
def test_query_instr(instruments):
    '''Testing the query_isa() for instrument type.
    '''
    query = net.query_isa("2022-12-05", "2022-12-07", instruments)
    for i in query: assert i['instrument'] == instruments, "The instrument in one or more of the query result does not match the input." 



@pytest.mark.parametrize('instruments', [('lir'), ('manannan'), ('fand'), ('ecne'),])
def test_query_startdate(instruments):
    '''Testing the query_isa() for the start date in the output dictionaries.
    '''
    query = net.query_isa("2022-12-05", "2022-12-07", instruments)
    assert query[0]['date'] == "2022-12-05", "The date of the first dictionary in the query results (the start date) is incorrect."



@pytest.mark.parametrize('instruments', [('lir'), ('manannan'), ('fand'), ('ecne'),])
def test_query_enddate(instruments):
    '''Testing the query_isa() for the end date.
    '''

    query = net.query_isa("2022-12-05", "2022-12-07", instruments)
    assert query[-1]['date'] == "2022-12-07", "The date of the last dictionary in the query results (the end date) is incorrect."




# Same tests but for default dates and instrument:


def test_default_query_keys():

    query = net.query_isa()  
    expected_query_keys = ['date', 'filename', 'instrument', 'resolution', 'time', 'xcoords',  'ycoords']

    for i in query: assert list( i.keys() ) == expected_query_keys, "One or more of the keys in one or more of the query result(s) is incorrect."


def test_default_query_keys(instruments):

    query = net.query_isa()  
    for i in query: assert (i['instrument']=='lir' or i['instrument']=='manannan' or i['instrument']=='fand' or i['instrument']=='ecne'), "The instrument in one or more of the query result does not match the input." 


def test_default_query_keys():
    todays_date = str( dt.today().strftime('%Y-%m-%d') ) # todays date using `datetime`
    
    query = net.query_isa()  
    assert query[0]['date'] == todays_date, "The date of the first dictionary in the query results (the start date) is incorrect."


def test_default_query_keys():
    todays_date = str( dt.today().strftime('%Y-%m-%d') ) 
    
    query = net.query_isa()  
    assert query[-2]['date'] == todays_date, "The date of the last dictionary in the query results (the end date) is incorrect."







########## NEGATIVE TESTS ###########


def test_query_err_startdate():
    """Test TypeError for start_date input
    """
    try:
        net.query_isa(start_date=123)
    except TypeError as e:
        assert str(e) == "The start date must be a string in the form YYYY-mm-dd."
    else:
        assert False, "TypeError not raised for start_date input."


def test_query_err_stopdate():
    """Test TypeError for stop_date input
    """
    try:
        net.query_isa(stop_date=456)
    except TypeError as e:
        assert str(e) == "The stop date must be a string in the form YYYY-mm-dd."
    else:
        assert False, "TypeError not raised for stop_date input."

def test_query_err_instr():
    """Test TypeError for instrument input
    """
    try:
        net.query_isa(instrument=789)
    except TypeError as e:
        assert str(e) == "The instrument name must be string."
    else:
        assert False, "TypeError not raised for instrument input."

def test_query_err_instr2():
    """Test ValueError for invalid instrument input
    """
    try:
        net.query_isa(instrument="invalid")
    except ValueError as e:
        assert str(e) == "Instrument not found. The four instruments are: 'lir', 'manannan', 'fand' and 'ecne'. The default value for this parameter is all 4."
    else:
        assert False, "ValueError not raised for invalid instrument input."


