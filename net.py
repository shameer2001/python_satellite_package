from requests import *

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

    payload = {'start_date':start_date, 'stop_date':stop_date, 'instrument': instrument}
    r=get('https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/', params=payload)

    return r.json()


def download_isa(filename, save_dir = None) -> None:
    # todo: Download the files from https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/
    ...


print(query_isa("2022-12-05", "2022-12-06", "lir") )
#print(type(query_isa("2022-12-05", "2022-12-06", "lir") ))