
class ISA:
    def __init__(self, date, filename, instrument, resolution, time, xcoords, ycoords):
        self.date = date
        self.fileName = filename
        self.instrument = instrument
        self.resolution = resolution
        self.time = time
        self.xCoords = xcoords
        self.yCoords = ycoords


def query_isa(start_date, stop_date, instrument) -> list[ISA]:
    # todo: Query the files from https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/
    #  return value shall be the list of ISA class
    ...


def download_isa(filename, save_dir) -> None:
    # todo: Download the files from https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/
    ...



