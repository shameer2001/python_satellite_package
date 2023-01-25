import sys
from aigeanpy.satmap import get_satmap
from aigeanpy.net import *

def aigean_mosaic(filelist, resolution = None):
    """ Create a mosaic by giving multiple filenames.

    Parameters
    ----------
    resolution: int, optional
                The resolution wanted for the output mosaic.
    filelist: list, positional
              A given filename or list of them, such as aigean_man_20221205_194510.hdf5 or aigean_fan_20221206_190424.zip

    Notes
    -----
    This function only accepts two or more filenames.

    """
    
    # check if all the files passed are valid Aigean images
    print(filelist)
    if len(filelist) < 2:
        raise ValueError("Only two or more filename inputs are acceptable.")
    invalid_files = []
    satmaps = []
    for file in filelist:
        try:
            download_file = download_isa(file)
            satmap = get_satmap(file)
            satmaps.append(satmap)
        except ValueError:
            invalid_files.append(file)

    if invalid_files:
        print("These files are not valid Aigean images:")
        for file in invalid_files:
            print(file)

    if len(satmaps) == 0:
        sys.stderr.write('No valid Aigean images')
        sys.exit(1)

    # mosaic the images
    mosaic_map = satmaps[0]
    for i in range(1, len(satmaps)):
        mosaic_map = mosaic_map.mosaic(satmaps[i], resolution) if resolution is not None else mosaic_map.mosaic(satmaps[i])

    # save the mosaic
    return mosaic_map.visualise(save=True)