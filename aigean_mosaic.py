import sys
from argparse import ArgumentParser
import requests
import json
from datetime import date
from datetime import timedelta
from satmap_copy import SatMap
from net_copy import net

def aigean_mosaic (filenames, resoltion = None):
    pass

def process_mosaic():
    parser = ArgumentParser(description='Creating a mosaic from the command line')
    parser.add_argument('--resolution', help= 'resolution argument')
    parser.add_argument('filename',type=str,nargs='+',help='input two or more file')    
    args_mosaic = parser.parse_args()
    obv = aigean_mosaic(args_mosaic.resolution, args_mosaic.filename)


if __name__ == "__main__":
    process_mosaic()
    