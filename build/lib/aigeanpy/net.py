from requests import *
from pathlib import Path

def query_isa(start_date = None, stop_date = None, instrument = None) -> list:
    """Returns a JSON file of the results from the query service.
        
    Parameters
    ----------
    start_date : str (date of format YYYY-mm-dd), optional
                    Look for data in query catalogue taken on this date and further. Default is the current date.

    stop_date : str (date of format YYYY-mm-dd), optional
                Look for data in query catalogue taken on this date and sooner. Default is the current date.
    
    
    instrument : str, optional
                One of the possible image-taking instruments: 'lir', 'manannan', 'fand' or 'csvfile'. The function only includes data taken with the select instrument. Default is None (ie. the function searches for all instruments).
                     
                     
    Notes
    -----
    A date is assigned to each data which represenets when the data was taken.
    Queries larger than 3 days are not allowed.

    
    
    
    Returns
    -------
    file: list
        Contains the data (each instant in a dictionary) extracted from the ISA archive. The file includes properties of the observations found in the specified time range and instruments (ie. the inputs)


    Examples:
    ---------

    >>> query_isa("2022-12-05", "2022-12-05", "lir")
    [{'date': '2022-12-05', 'filename': 'aigean_lir_20221205_191610.asdf', 'instrument': 'lir', 'resolution': 30, 'time': '19:16:10', 'xcoords': [500.0, 1100.0], 'ycoords': [200.0, 500.0]}, {'date': '2022-12-05', 'filename': 'aigean_lir_20221205_194510.asdf', 'instrument': 'lir', 'resolution': 30, 'time': '19:45:10', 'xcoords': [800.0, 1400.0], 'ycoords': [100.0, 400.0]}]
    >>> query_isa("2022-12-06", "2022-12-07", "fand")
    [{'date': '2022-12-06', 'filename': 'aigean_ecn_20221206_181924.csv', 'instrument': 'ecne', 'resolution': 1, 'time': '18:19:24', 'xcoords': [0.0, 1500.0], 'ycoords': [0.0, 500.0]}, {'date': '2022-12-07', 'filename': 'aigean_ecn_20221207_172238.csv', 'instrument': 'ecne', 'resolution': 1, 'time': '17:22:38', 'xcoords': [0.0, 1500.0], 'ycoords': [0.0, 500.0]}]
    >>> query_isa("2023-01-05", "2023-01-05")
    [{'date': '2023-01-05', 'filename': 'aigean_lir_20230105_135624.asdf', 'instrument': 'lir', 'resolution': 30, 'time': '13:56:24', 'xcoords': [500.0, 1100.0], 'ycoords': [0.0, 300.0]}, {'date': '2023-01-05', 'filename': 'aigean_lir_20230105_142424.asdf', 'instrument': 'lir', 'resolution': 30, 'time': '14:24:24', 'xcoords': [700.0, 1300.0], 'ycoords': [0.0, 300.0]}, {'date': '2023-01-05', 'filename': 'aigean_man_20230105_135624.hdf5', 'instrument': 'manannan', 'resolution': 15, 'time': '13:56:24', 'xcoords': [0.0, 450.0], 'ycoords': [200.0, 350.0]}, {'date': '2023-01-05', 'filename': 'aigean_man_20230105_141024.hdf5', 'instrument': 'manannan', 'resolution': 15, 'time': '14:10:24', 'xcoords': [600.0, 1050.0], 'ycoords': [250.0, 400.0]}, {'date': '2023-01-05', 'filename': 'aigean_man_20230105_142524.hdf5', 'instrument': 'manannan', 'resolution': 15, 'time': '14:25:24', 'xcoords': [900.0, 1350.0], 'ycoords': [150.0, 300.0]}, {'date': '2023-01-05', 'filename': 'aigean_man_20230105_144124.hdf5', 'instrument': 'manannan', 'resolution': 15, 'time': '14:41:24', 'xcoords': [1050.0, 1500.0], 'ycoords': [250.0, 400.0]}, {'date': '2023-01-05', 'filename': 'aigean_fan_20230105_135624.zip', 'instrument': 'fand', 'resolution': 5, 'time': '13:56:24', 'xcoords': [0.0, 225.0], 'ycoords': [400.0, 450.0]}, {'date': '2023-01-05', 'filename': 'aigean_fan_20230105_140124.zip', 'instrument': 'fand', 'resolution': 5, 'time': '14:01:24', 'xcoords': [150.0, 375.0], 'ycoords': [350.0, 400.0]}, {'date': '2023-01-05', 'filename': 'aigean_fan_20230105_140724.zip', 'instrument': 'fand', 'resolution': 5, 'time': '14:07:24', 'xcoords': [375.0, 600.0], 'ycoords': [400.0, 450.0]}, {'date': '2023-01-05', 'filename': 'aigean_fan_20230105_141424.zip', 'instrument': 'fand', 'resolution': 5, 'time': '14:14:24', 'xcoords': [450.0, 675.0], 'ycoords': [200.0, 250.0]}, {'date': '2023-01-05', 'filename': 'aigean_fan_20230105_142124.zip', 'instrument': 'fand', 'resolution': 5, 'time': '14:21:24', 'xcoords': [675.0, 900.0], 'ycoords': [450.0, 500.0]}, {'date': '2023-01-05', 'filename': 'aigean_fan_20230105_142624.zip', 'instrument': 'fand', 'resolution': 5, 'time': '14:26:24', 'xcoords': [750.0, 975.0], 'ycoords': [250.0, 300.0]}, {'date': '2023-01-05', 'filename': 'aigean_fan_20230105_143124.zip', 'instrument': 'fand', 'resolution': 5, 'time': '14:31:24', 'xcoords': [900.0, 1125.0], 'ycoords': [400.0, 450.0]}, {'date': '2023-01-05', 'filename': 'aigean_fan_20230105_143724.zip', 'instrument': 'fand', 'resolution': 5, 'time': '14:37:24', 'xcoords': [975.0, 1200.0], 'ycoords': [200.0, 250.0]}, {'date': '2023-01-05', 'filename': 'aigean_fan_20230105_144424.zip', 'instrument': 'fand', 'resolution': 5, 'time': '14:44:24', 'xcoords': [1125.0, 1350.0], 'ycoords': [300.0, 350.0]}, {'date': '2023-01-05', 'filename': 'aigean_ecn_20230105_135624.csv', 'instrument': 'ecne', 'resolution': 1, 'time': '13:56:24', 'xcoords': [0.0, 1500.0], 'ycoords': [0.0, 500.0]}]



    
    
    """
    # Error messages for incorrect inputs:
         
    if type(start_date) != str and start_date != None:
        raise TypeError("The start date must be a string in the form YYYY-mm-dd.")
            
    if type(stop_date) != str and stop_date != None:
        raise TypeError("The stop date must be a string in the form YYYY-mm-dd.")
            
    if type(instrument) != str and (instrument != None):
        raise TypeError("The instrument name must be string.")
        
    if instrument != 'lir' and instrument != 'manannan' \
    and instrument != 'fand' and  instrument != 'ecne' and instrument != None: \
         raise ValueError("Instrument not found. The four instruments are: 'lir', 'manannan', 'fand' and 'ecne'. The default value for this parameter is all 4.")



    # Obtain data:
        
    payload = {'start_date':start_date, 'stop_date':stop_date, 'instrument': instrument}
    r=get('https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/', params=payload)



    # Print errors from json file:
    for i in r.json():
        if i=='message':
            error_message = r.json()['message']
            raise ValueError(error_message) # raise errors built-in to the archive query service
        
        else:
            print(r.json())
            return r.json() # Return json for testing

        
    # Raise error if empty query results (likely due to no data in given data range):
    if r.content == b'[]\n':
        raise ValueError("There is no data available on this date for the instrument(s) selected.")

    
        


        
def download_isa(filename, save_dir = None) -> None:
    """Downloads the data from the search done by the `net.query_isa()` function.


    Parameters
    ----------
    filename : str
                Name of a file as provided by the `net.query_isa()` function.
    

    
    
    save_dir : str or path object, optional
                The directory to save the file in. Default is None (ie download to current working directory)
                
    
    """

    # Error messages for incorrect inputs:
    if type(filename) != str:
        raise TypeError("The filename must be a string.")
                       
    if type(save_dir) != str and save_dir != None:
        raise TypeError("The `save_dir` variable is not a string.")



    if save_dir:
        p = Path('{}/{}'.format(save_dir, filename))
            
            
        if not Path(save_dir).exists(): # if no such path exists
            raise NotADirectoryError("The directory given, for the `save_dir` variable, does not exist.")
                
    else:
        p = Path(filename) # with full name to save with correct extension



    # Obtain request from server:
    payload = {'filename':filename}
    r = get('https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/download/', params=payload)

    p.write_bytes(r.content) #download



#print(net.query_isa("2022-12-05", "2022-12-06", "lir") )
#print(type(query_isa("2022-12-05", "2022-12-06", "lir") ))

# download_isa("aigean_lir_20221205_191610.asdf")
# import json
# import numpy as np
#query = net.query_isa()
#query = net.query_isa("2022-12-05", "2022-12-06", "lir")

#print(query)

#query = json.load(query)
#print(np.array(query))
#print(type(query))

#print(query[-1])

#query_isa("2022-12-05", "2022-12-05", "lir")
#query_isa("2022-12-06", "2022-12-07", "ecne")
#query_isa("2023-01-05", "2023-01-05")