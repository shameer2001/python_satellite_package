from argparse import ArgumentParser
from aigeanpy.satmap import SatMap, get_satmap
from aigeanpy.net import net
from datetime import date

def aigean_metadata(filenames):
    """ Extractin the metadata information from correct files, and show the uncorrect files name below

    Parameters
    ----------
    filenames: list, positional
        A given filename or list of them, such as aigean_man_20221205_194510.hdf5 or aigean_fan_20221206_190424.zip

    Notes
    ----------
    This function take a 'aigean' file without (9 sets of key and meta data value) as a corrypted one

    Returns
    ----------
    outputs: str
        the set of meta information outputs(key:value) of given files, and name of files failed to process

    Examples
    ----------
    >>> from aigean_metadata import aigean_metadata
    >>> aigean_metadata(['aigean_man_20221205_194510.hdf5','aigean_fan_20221205_192210.zip','asadasf.py'])
    aigean_man_20221205_194510.hdf5:archive: ISA
    aigean_man_20221205_194510.hdf5:observatory: Aigean
    aigean_man_20221205_194510.hdf5:instrument: Manannan
    aigean_man_20221205_194510.hdf5:obs_date: 2022-12-05 19:45:10
    aigean_fan_20221205_192210.zip:year: 2023
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
    for i in filenames:
        # filter input in wrong type
        if type(i) != str:
            raise TypeError("name of files inpute must be string")
        # filter inputs are not in right file format (e.g. xxxxx.xxx) 
        if len(i.split('.')) != 2:
            raise ValueError("name of files should in right format")
        # filter inputs with wrong date format in file name (e.g. 1332)
        if int(i.split('_')[2][4:6]) > 12 or int(i.split('_')[2][6:8]) > 31:
            raise ValueError("date in file name is wrong")

        
    # create this list to collect file names are corrupted or failed to process 
    error_file = []
    # create test_dist to collect first 4 key elements for testing purpose
    test_dict = {}
    if len(filenames) == 1:
        for i in filenames:
            filename = i
            filetype = filename.split('.')[1]
            # filter file with wrong type
            if filetype in ('asdf','hdf5','zip'):
                download_form = filename.split('_')[0]
                # to see if the file is downloaded from 'aigean' file
                if download_form in ('aigean'):
                    download_file = net.download_isa (filename)
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

            return test_dict
    
    else:
        for i in filenames:
            filename = i
            filetype = filename.split('.')[1]
            # filter file with wrong type
            if filetype in ('asdf','hdf5','zip'):
                download_form = filename.split('_')[0]
                # to see if the file is downloaded from 'aigean' file
                if download_form in ('aigean'):
                    download_file = net.download_isa (filename)
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
        for i in range(len(error_file)):
            print (' - {}'.format(error_file[i]))
        return
# test sample
x =aigean_metadata(['aigean_man_20221205_194510.hdf5','aigean_fan_20221206_190424.zip'])
# x =aigean_metadata(['aigean_man_20221205_194510.hdf5'])



    
