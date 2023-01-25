from datetime import date
from datetime import timedelta

import requests

from aigeanpy.net import *
from aigeanpy.satmap import SatMap, get_satmap


def aigean_today(instrument = None, saveplot=False):
    """ Getting the latest image from the archive.

    Parameters
    ----------
    instrument: str, optional
        An optional specification: choose from 4 different intruments('lir','manannan','fand','ecne'), or leave it along as None to get the last 
        observation(with no specific instrument requirement)
    saveplot: bool, optional
        The save = False as default setting. If save is set to True, then the image should not be displayed on the screen and saved in the required
        path. If save is set to False, the image should be displayed on the screen, but not get saved in the directory.
    
    Notes
    -----
    The data file and image(if there is one) will be saved in the directory where it is run.
    """
    # use 'datetime' from python standard library to get the date of today and the most recent update date
    # Cause sometimes the achive don't update constantly for several date, so we have to get the most recent date with updates
    if instrument != None:
        if type(instrument) != str:
            raise TypeError("name of instrument input must be string")
        if instrument not in ('lir','manannan','fand','ecne'):
            raise ValueError("name of instrument input is not available")
    d = 0
    text = {}
    while len(text) < 4:
        today = date.today()
        # find the most recent date with data updating 
        most_recent_date = today - timedelta(days = d)
        # Set params in the request, if the instrument is not specified then it will download the most recent obsevation
        if instrument != None:
            param = {'start_date':most_recent_date,'stop_date':most_recent_date,'instrument':str(instrument)}
            response = requests.get(
                "http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/?",
                params=param)
            text = response.text
        else:
            param = {'start_date':most_recent_date,'stop_date':most_recent_date}
            response = requests.get(
                "http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/?",
                params=param)
            text = response.text
        d += 1
    # transform type of text from str to list
    most_recent_date_update = eval(text)
    date_list = []
    # find the most recent observation
    for i in range(len(most_recent_date_update)):
        date_list.append(most_recent_date_update[i]['time'])
    most_recent_obv_index = date_list.index(max(date_list))
    most_recent_obv = most_recent_date_update[most_recent_obv_index]
    # download file to current working directory
    download_file = download_isa (most_recent_obv['filename'])

    if saveplot == True:  
        if most_recent_obv['instrument'] != 'ecne':
            read_file = get_satmap(most_recent_obv['filename'])
            # extract all key data from file
            meta = read_file.meta
            data = read_file.data
            fov = read_file.fov
            shape = read_file.shape
            centre = read_file.centre
            satmap_file = SatMap(meta=meta, data=data, shape=shape, fov=fov, centre=centre)
            # save the image in the directory where it's run
            save_image = satmap_file.visualise(True,'')
            print ('message: the file downloaded can be visulised, the image is downloaded in the directory where it is run')
            return
        else:            
            return print ('message: the file downloaded cannot be visulised')
    else:
        # if the --saveplot flag is not passed, we try to show the plot if the file is visualble, and download data in the directory where it is run.
        if most_recent_obv['instrument'] != 'ecne':
            read_file = get_satmap(most_recent_obv['filename'])
            meta = read_file.meta
            data = read_file.data
            fov = read_file.fov
            shape = read_file.shape
            centre = read_file.centre
            satmap_file = SatMap(meta=meta, data=data, shape=shape, fov=fov, centre=centre)
            # save the image in the directory where it's run
            show_image = satmap_file.visualise(False,'')
            return print('message: the file downloaded can be visulised, the image is showed')
        else:
            return print ('message: the file downloaded cannot be visulised')

