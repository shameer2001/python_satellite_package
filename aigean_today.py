import sys
from argparse import ArgumentParser
import requests
import json
from datetime import date
from datetime import timedelta
# from net import query_isa, download_isa
# from satmap import get_satmap


def aigean_today(instrument = '', saveplot=False):
    """
    Getting the latest image of the archive
    ---------
    instrument: str
        An optional specification: choose for 4 different intruments('lir','manannan','fand','ecne'), or leave it along as None for the last observation(with any instrument)
    saveplot: bool
        Ture for save the png image(except with the instrument 'ecne'), False for not save the png image. (False as default)
    Returns
    ---------
        PNG_figure and data downloaded in the local directory
    """
    # use 'datetime' from python standard library to get the date of today and the most recent update date
    # Cause sometimes the achive don't update constantly for several date, so we have to get the most recent date with updates
    # if type(instrument) != str:
    #     raise TypeError("names of instrument inpute must be string")
    # print(instrument)
    if instrument != None:
        if instrument not in ('lir','manannan','fand','ecne'):
            raise ValueError("names of instrument inpute is not available")
    d = 0
    text = {}
    while len(text) < 4:
        today = date.today()
        most_recent_date = today - timedelta(days = d)
        # Set params in the request, if the instrument is not specified then it will download the most recent obsevation
        # the reason why we also put yesterday's date is because
        if instrument != None:
            ## use the function from net.py after commit
            #response = query_isa(most_recent_date, most_recent_date, instrument)

            param = {'start_date':most_recent_date,'stop_date':most_recent_date,'instrument':str(instrument)}
            response = requests.get(
                "http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/?",
                params=param)
            text = response.text
        else:
            ## use the function from net.py after commit
            # response = query_isa(most_recent_date, most_recent_date,'')
            param = {'start_date':most_recent_date,'stop_date':most_recent_date}
            response = requests.get(
                "http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/?",
                params=param)
            text = response.text
        d += 1
    # transform type of text from str to list
    most_recent_date_update = eval(text)
    date_list = []
    for i in range(len(most_recent_date_update)):
        date_list.append(most_recent_date_update[i]['time'])
    most_recent_obv_index = date_list.index(max(date_list))
    most_recent_obv = most_recent_date_update[most_recent_obv_index]
    # print(type(most_recent_obv))
    # print(len(info))
    # print(info[15]['date'])
    download_file = requests.get('http://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/download/?',
                    params= {'filename':most_recent_obv['filename']})
    ## use the function from net.py after shameer commit, it should save the downloaded file rightaway
    # download_file = download_isa (most_recent_obv['filename'])
    
    if saveplot == True:  
        if most_recent_obv['instrument'] != 'ecne':
            # wait for the visulise function
            print('save the last image')
        else:            
            print ('message: the file downloaded cannot be visulised')
    else:
        # save the download
        print('save the download in directory')
    return
# aigean_today('ecne',saveplot=True)

def process_today():
    parser = ArgumentParser(description='Generate the last observation data ot image')

    parser.add_argument('--instrument','-i', help= 'Specified instrument')
    parser.add_argument('--saveplot','-s',action="store_true", help='Determined whether we want to generate a png')
    
    args_today = parser.parse_args()
    obv = aigean_today(args_today.instrument, args_today.saveplot)
    print(obv)


 

if __name__ == "__main__":
    process_today()