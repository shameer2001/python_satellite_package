
import sys


def aigean_today(instrument, saveplot):
    # todo: Getting the latest image of the archive,
    #  download the most recent data taken by a specified instrument and create or downloaded in the directory
    ...


def aigean_metadata(filename, **kwargs):
    # todo: given the list of file, extracting the metadata information
    ...


def aigean_mosaic(filename, **kwargs):
    # todo: Creating a mosaic from the command line
    ...


if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])