from aigeanpy.satmap import get_satmap
from aigeanpy.net import *
from datetime import date
import os

def aigean_metadata(filenames) -> list:
    """ Extracting the meta-data information from files and showing invalid files.

    Parameters
    ----------
    filenames: list, positional
        A given filename or list of them, such as aigean_man_20221205_194510.hdf5 or aigean_fan_20221206_190424.zip

    Notes
    -----
    This function takes an 'aigean' file, without 9 sets of key and meta data value, as a corrupted one.

    Returns
    -------
    outputs: dict
        The set of meta information. It outputs (key:value) for the given files, and the name of files failed to process.

    Examples
    ----------
    >>> from aigeanpy.aigean_metadata import aigean_metadata
    >>> aigean_metadata(['aigean_man_20221205_194510.hdf5','aigean_fan_20221205_192210.zip','asadasf.py'])
    aigean_man_20221205_194510.hdf5:archive: ISA
    aigean_man_20221205_194510.hdf5:observatory: Aigean
    aigean_man_20221205_194510.hdf5:instrument: Manannan
    aigean_man_20221205_194510.hdf5:obs_date: 2022-12-05 19:45:10
    aigean_man_20221205_194510.hdf5:year: 2023
    aigean_man_20221205_194510.hdf5:resolution: 15
    aigean_man_20221205_194510.hdf5:xcoords: [ 750. 1200.]
    aigean_man_20221205_194510.hdf5:ycoords: [250. 400.]
    aigean_fan_20221205_192210.zip:archive: ISA
    aigean_fan_20221205_192210.zip:observatory: Aigean
    aigean_fan_20221205_192210.zip:instrument: Fand
    aigean_fan_20221205_192210.zip:obs_date: 2022-12-05 19:22:10
    aigean_fan_20221205_192210.zip:year: 2023
    aigean_fan_20221205_192210.zip:resolution: 5
    aigean_fan_20221205_192210.zip:xcoords: [300.0, 525.0]
    aigean_fan_20221205_192210.zip:ycoords: [50.0, 100.0]
    These files failed while being processed
     - asadasf.py
    """

    # input must be a list (even if one file):
    if type(filenames) != list and type(filenames) != str:
        raise TypeError("Input filename(s) must be in a list (if multiple) or a string (if single).")


    if type(filenames) == list and len(filenames) > 1: # for multiple files and command-line
        for i in filenames:
            # filter input in wrong type
            if type(i) != str:
                raise TypeError("Name of files input must be string.")
                
            # filter inputs are not in right file format (e.g. xxxxx.xxx) 
            filetype = os.path.splitext(i)[1]  # obtain file extension


    elif type(filenames) == list and len(filenames) == 1: # for one list input
        for i in filenames:
            print(i)
            # filter input in wrong type
            if type(i) != str:
                raise TypeError("Name of files input must be string.")
                
            # filter inputs are not in right file format (e.g. xxxxx.xxx) 
            filetype = os.path.splitext(i)[1]  # obtain file extension

            if filetype != '.asdf' \
                and filetype != '.hdf5' \
                    and filetype != '.zip':
                    raise NameError("The file format is not supported. Only these are accepted: ASDF, HDF5 and ZIP.")
    


    elif type(filenames) != list : # if only 1 file

        if type(filenames) != str:
            raise TypeError("Name of files input must be string.")
                
        # filter inputs are not in right file format (e.g. xxxxx.xxx) 
        filetype = os.path.splitext(str(filenames))[1]  # obtain file extension
            
        if filetype != '.asdf' \
            and filetype != '.hdf5' \
                and filetype != '.zip':
                raise NameError("The file format is not supported. Only these are accepted: ASDF, HDF5 and ZIP.")
 

        
    # create this list to collect file names are corrupted or failed to process 
    error_file = []
    # create test_dist to collect first 4 key elements for testing purpose
    test_dict = {}
    if len(filenames) == 1: # command-line single file
        for i in filenames:
            filename = i
            filetype = filename.split('.')[1]
            # filter file with wrong type
            if filetype in ('asdf','hdf5','zip'):
                download_form = filename.split('_')[0]
                # to see if the file is downloaded from 'aigean' file
                if download_form in ('aigean'):
                    download_file = download_isa (filename)
                    satmap_file = get_satmap(filename)
                    meta_data = satmap_file.meta
                    # to check if the file is corrupted and missed meta data
                    # we take the file with less than 9 keys as corrupted
                    if len(meta_data) >= 9:
                        ## use the function get_map after branch merger
                        archive = meta_data['archive']
                        obv = meta_data['observatory']
                        instrument = meta_data['instrument']
                        obs_date = meta_data['date'] + ' ' + meta_data['time']
                        year = meta_data['year']
                        resolution = meta_data['resolution']
                        xcoords = meta_data['xcoords'] 
                        ycoords = meta_data['ycoords']
                        date_metadata = meta_data['date']
                        test_dict = {'archive:': archive, 'observatory:': obv, 'instrument:': instrument, 'obs_date:': obs_date}
                        # filter file with wrong date information in mate data
                        if int(date_metadata.split('-')[1]) > 12 or int(date_metadata.split('-')[2]) > 31:
                            print('These files failed while being processed')
                            print(' - {}'.format(filename))
                        elif str(date.today()) < date_metadata:
                            print('These files failed while being processed')
                            print(' - {}'.format(filename))  
                        else:                 
                            print ('archive:', archive)
                            print ('observatory:', obv)
                            print ('instrument:', instrument)
                            print ('obs_date:', obs_date)
                            print ('year:', year)
                            print ('resolution:', resolution)
                            print ('xcoords:', xcoords)
                            print ('ycoords:', ycoords)
                    
                    else:
                        print('These files failed while being processed')
                        print(' - {}'.format(filename))
                       
            else:
                print('These files failed while being processed')
                print(' - {}'.format(filename))

            #return test_dict

    elif type(filenames) == str: # single file from import module into .py
        filename = filenames
        filetype = filename.split('.')[1]
        # filter file with wrong type
        if filetype in ('asdf','hdf5','zip'):
            download_form = filename.split('_')[0]
            # to see if the file is downloaded from 'aigean' file
            if download_form in ('aigean'):
                download_file = download_isa (filename)
                satmap_file = get_satmap(filename)
                meta_data = satmap_file.meta
                # to check if the file is corrupted and missed meta data
                # we take the file with less than 9 keys as corrupted
                if len(meta_data) >= 9:
                    ## use the function get_map after branch merger
                    archive = meta_data['archive']
                    obv = meta_data['observatory']
                    instrument = meta_data['instrument']
                    obs_date = meta_data['date'] + ' ' + meta_data['time']
                    year = meta_data['year']
                    resolution = meta_data['resolution']
                    xcoords = meta_data['xcoords'] 
                    ycoords = meta_data['ycoords']
                    date_metadata = meta_data['date']
                    test_dict = {'archive:': archive, 'observatory:': obv, 'instrument:': instrument, 'obs_date:': obs_date}
                    # filter file with wrong date information in mate data
                    if int(date_metadata.split('-')[1]) > 12 or int(date_metadata.split('-')[2]) > 31:
                        print('These files failed while being processed')
                        print(' - {}'.format(filename))
                    elif str(date.today()) < date_metadata:
                        print('These files failed while being processed')
                        print(' - {}'.format(filename))  
                    else:                 
                        print ('archive:', archive)
                        print ('observatory:', obv)
                        print ('instrument:', instrument)
                        print ('obs_date:', obs_date)
                        print ('year:', year)
                        print ('resolution:', resolution)
                        print ('xcoords:', xcoords)
                        print ('ycoords:', ycoords)
                    
                else:
                    print('These files failed while being processed')
                    print(' - {}'.format(filename))
                       
        else:
            print('These files failed while being processed')
            print(' - {}'.format(filename))

        #return test_dict
    
    else: #multiple files
        for i in filenames:
            filename = i
            filetype = filename.split('.')[1]
            # filter file with wrong type
            if filetype in ('asdf','hdf5','zip'):
                download_form = filename.split('_')[0]
                # to see if the file is downloaded from 'aigean' file
                if download_form in ('aigean'):
                    download_file = download_isa (filename)
                    satmap_file = get_satmap(filename)
                    meta_data = satmap_file.meta
                    # to check if the file is corrupted and missed meta data, we see file with less than 9 key elements as a corrupted one
                    if len(meta_data) >= 9:               
                        # extract 9 key elements
                        archive = meta_data['archive']
                        obv = meta_data['observatory']
                        instrument = meta_data['instrument']
                        obs_date = meta_data['date'] + ' ' + meta_data['time']
                        resolution = meta_data['resolution']
                        year = meta_data['year']
                        xcoords = meta_data['xcoords'] 
                        ycoords = meta_data['ycoords']
                        date_metadata = meta_data['date']
                        # filter file with wrong date information in meta data
                        if int(date_metadata.split('-')[1]) > 12 or int(date_metadata.split('-')[2]) > 31:
                            error_file.append(filename)
                        # filter file with wrong date information in meta data
                        elif str(date.today()) < date_metadata:
                            error_file.append(filename)
                        else:
                            print ('{}:archive: {}'.format(filename,archive))
                            print ('{}:observatory: {}'.format(filename,obv))
                            print ('{}:instrument: {}'.format(filename,instrument))
                            print ('{}:obs_date: {}'.format(filename,obs_date))
                            print ('{}:year: {}'.format(filename,year))
                            print ('{}:resolution: {}'.format(filename,resolution))
                            print ('{}:xcoords: {}'.format(filename,xcoords))
                            print ('{}:ycoords: {}'.format(filename,ycoords))
                    else:
                        error_file.append(filename)
                else:
                    error_file.append(filename)
            else:
                error_file.append(filename)
        # list of the files that were corrupted or failed to process, and print them out
        print('These files failed while being processed')
        for i in error_file:
            print (' - {}'.format(i))
        #return test_dict