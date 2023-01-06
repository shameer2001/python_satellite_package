from requests import *
from pathlib import Path

class net:
    def __init__(self, date, filename, instrument, resolution, time, xcoords, ycoords):
        self.date = date
        self.fileName = filename
        self.instrument = instrument
        self.resolution = resolution
        self.time = time
        self.xCoords = xcoords
        self.yCoords = ycoords


def query_isa(start_date = None, stop_date = None, instrument = None) -> list[net]:
    """Returns a JSON file of the results from the query service. 


    Parameters
    ----------
    start_date : str (date of format YYYY-mm-dd), optional
                 Look for data in query catalogue taken on this date and further. Default is the current date.
    
    stop_date : str (date of format YYYY-mm-dd), optional
                Look for data in query catalogue taken on this date and sooner. Default is the current date.
    
    
    instrument : str, optional
                 One of the possible image-taking instruments: 'lir', 'manannan', 'fand' or 'csvfile'. The function only includes data taken with the select instrument. Default is None (ie. the function searches for all).


    Notes
    -----
    A date is assigned to each data which represenets when the data was taken.
    Queries larger than 3 days are not allowed.

    
    
    
    
    Returns
    -------
    file: list
          Contains the data (each instant in a dictionary) extracted from the ISA archive. The file includes properties of the observations found in the specified time range and instruments (ie. the inputs)
    
    
    """

    payload = {'start_date':start_date, 'stop_date':stop_date, 'instrument': instrument}
    r=get('https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/', params=payload)

    return r.json()


def download_isa(filename, save_dir = None) -> None:
    """Returns a JSON file of the results from the query service. 


    Parameters
    ----------
    start_date : str (date of format YYYY-mm-dd), optional
                 Look for data in query catalogue taken on this date and further. Default is the current date.
    
    stop_date : str (date of format YYYY-mm-dd), optional
                Look for data in query catalogue taken on this date and sooner. Default is the current date.
    
    
    instrument : str, optional
                 One of the possible image-taking instruments: 'lir', 'manannan', 'fand' or 'csvfile'. The function only includes data taken with the select instrument. Default is None (ie. the function searches for all).


    Notes
    -----
    A date is assigned to each data which represenets when the data was taken.
    Queries larger than 3 days are not allowed.

    
    
    
    
    Returns
    -------
    file: list
          Contains the data (each instant in a dictionary) extracted from the ISA archive. The file includes properties of the observations found in the specified time range and instruments (ie. the inputs)
    
    
    """
    
    p = Path(filename)

    payload = {'filename':filename}
    r = get('https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/download/', params=payload)

    p.write_bytes(r.content) #download

print(query_isa("2022-12-05", "2022-12-06", "lir") )
#print(type(query_isa("2022-12-05", "2022-12-06", "lir") ))

download_isa("aigean_lir_20221205_191610.asdf")