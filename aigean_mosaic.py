import sys
import argparse
from satmap import get_satmap

def aigean_mosaic():
    parser = argparse.ArgumentParser(description='Mosaic multiple Aigean images')
    parser.add_argument('filelist', metavar='file', type=str, nargs='+',
                        help='List of files to be used for mosaic')
    parser.add_argument('-r', '--resolution', type=int, default=30,
                        help='Resolution of the final mosaic')
    args = parser.parse_args()

    files = args.filelist
    resolution = args.resolution

    
    # check if all the files passed are valid Aigean images
    invalid_files = []
    satmaps = []
    for file in files:
        try:
            satmap = get_satmap(file)
            satmaps.append(satmap)
        except:
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
        mosaic_map = mosaic_map.mosaic(satmaps[i], resolution)

    # save the mosaic
    mosaic_map.visualise(save=True)

if __name__ == "__main__":
    aigean_mosaic()
