import sys
from argparse import ArgumentParser
import requests
import json
from datetime import date
from datetime import timedelta
from satmap_copy import SatMap
from net_copy import net
def aigean_metadata(args):
    # todo: given the list of file, extracting the metadata information
    ...
    # print(len(args),type(args))
    error_file = []
    if len(args) == 1:
        for i in args:
            filename = i
            filetype = filename.split('.')[1]
            if filetype in ('asdf','hdf5','zip'):
                download_form = filename.split('_')[0]
                # to see if the file is downloaded from 'aigean' file
                if download_form in ('aigean'):
                    # print(filename, type(filename))
                    download_file = net.download_isa (filename)
                    # download_file = requests.get('http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/download/?',
                    #                 params= {'filename':str(kwargs)})
                    satmap_file = SatMap(filename)
                    print(download_file)
                    meta_data = satmap_file.meta()
                    print(len(meta_data))
                    print(meta_data)
                    if len(meta_data) == 9:
                        ## use the function get_map after branch merger
                        archive = meta_data['archive']
                        obv = meta_data['observatory']
                        instrument = meta_data['instrument']
                        obs_date = meta_data['date'] + ' ' + meta_data['time']
                        resolution = meta_data['resolution']
                        xcoords = meta_data['xcoords'] 
                        ycoords = meta_data['ycoords']
                        print('archive:', archive)
                        print('observatory:', obv)
                        print('instrument:', instrument)
                        print('obs_date:', obs_date)
                        print ('resolution:', resolution)
                        print ('xcoords:', xcoords)
                        print ('ycoords:', ycoords)
                    
                    else:
                        print('These files failed while being processed')
                        print(' - {}'.format(filename))
                       
            else:
                print('These files failed while being processed')
                print(' - {}'.format(filename))
            return
    
    else:
        for i in args:
            filename = i
            filetype = filename.split('.')[1]
            if filetype in ('asdf','hdf5','zip'):
                download_form = filename.split('_')[0]
                if download_form in ('aigean'):
                    # print(filename, type(filename))
                    download_file = net.download_isa (filename)
                    # download_file = requests.get('http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/download/?',
                    #                 params= {'filename':str(kwargs)})
                    satmap_file = SatMap(filename)
                    meta_data = satmap_file.meta()
                    # to check if the file is corrupted, which missed meta data
                    if len(meta_data) == 9:               
                        ## use the function get_map after
                        archive = meta_data['archive']
                        obv = meta_data['observatory']
                        instrument = meta_data['instrument']
                        obs_date = meta_data['date'] + ' ' + meta_data['time']
                        resolution = meta_data['resolution']
                        xcoords = meta_data['xcoords'] 
                        ycoords = meta_data['ycoords']
                        # print(meta_data)
                        print ('{}:archive: {}'.format(filename,archive))
                        print ('{}:observatory: {}'.format(filename,obv))
                        print ('{}:instrument: {}'.format(filename,instrument))
                        print ('{}:obs_date: {}'.format(filename,obs_date))
                        print ('{}:resolution: {}'.format(filename,resolution))
                        print ('{}:xcoords: {}'.format(filename,xcoords))
                        print ('{}:ycoords: {}'.format(filename,ycoords))
                    else:
                        error_file.append(filename)
                else:
                    error_file.append(filename)
            else:
                error_file.append(filename)
        # list of the files that were incorrectly read
        print('These files failed while being processed')
        # print(error_file)
        for i in range(len(error_file)):
            print (' - {}'.format(error_file[i]))
        return
# x = aigean_metadata('aigean_man_20221205_194510.hdf5','aigean_fan_20221206_190424.zip', 'aigean_fan_20221205_192210.zip')

def process_metadata():
    parser = ArgumentParser(description='Extracting the file metadata information')
    parser.add_argument('filename',type=str,nargs='+',help='input a file or list of them')
    args_metadata = parser.parse_args()
    obv = aigean_metadata(args_metadata.filename)
    # print(obv)


 

if __name__ == "__main__":
    process_metadata()
    
