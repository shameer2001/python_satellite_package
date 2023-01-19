from argparse import ArgumentParser
from aigeanpy.aigean_today import aigean_today
from aigeanpy.aigean_metadata import aigean_metadata

# command line interface setting
def process_today():
    parser = ArgumentParser(description='Generate the last observation data ot image')

    parser.add_argument('--instrument','-i', help= 'Specified instrument')
    parser.add_argument('--saveplot','-s',action="store_true", help='Determined whether we want to generate a png')
    
    args_today = parser.parse_args()
    obv = aigean_today(args_today.instrument, args_today.saveplot)

def process_metadata():
    parser = ArgumentParser(description='Extracting the file metadata information')
    parser.add_argument('filenames',type=str,nargs='+',help='input a file or list of them')
    args_metadata = parser.parse_args()
    obv = aigean_metadata(args_metadata.filenames)

def process_metadata():
    parser = argparse.ArgumentParser(description='Mosaic multiple Aigean images')
    parser.add_argument('filelist', metavar='file', type=str, nargs='+',
                        help='List of files to be used for mosaic')
    parser.add_argument('-r', '--resolution', type=int, default=30,
                        help='Resolution of the final mosaic')
    args = parser.parse_args()


if __name__ == "__main__":
    process_metadata()
    process_today()