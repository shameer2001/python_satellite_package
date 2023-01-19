import sys
import argparse
from aigeanpy.satmap import get_satmap
from aigeanpy.net import net

def aigean_mosaic(filelist, resolution = None):
    
    # check if all the files passed are valid Aigean images
    print(filelist)
    if len(filelist) < 2:
        raise ValueError("only two or more filename inputs are acceptable")
    invalid_files = []
    satmaps = []
    for file in filelist:
        try:
            download_file = net.download_isa (file)
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
    mosaic_map.visualise(save=True)
    return 

# x = aigean_mosaic(['aigean_lir_20230105_135624.asdf', 'aigean_lir_20230105_142424.asdf'])