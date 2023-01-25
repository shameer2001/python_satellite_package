
from aigeanpy.net import *
import h5py
import asdf
import json
import csv
from zipfile import ZipFile
import numpy as np
import os 
from io import BytesIO

def read(file):
    """Extracts the data and meta data from the input file.


    Parameters
    ----------
    file: str
          The name of the file or path to the file. 
    


    Notes
    -----
    
    Each of the instruments used different file formats to store the data and meta data;
        - Lir uses Advanced Scientific Data Format (ASDF). File extension: '.asdf'   
        - Manannn uses Hierarchical Data Format 5 (HDF5). 
        - Fand stores the data in 'npy' format and the meta data in JSON files.
        - Ecne measures turbulence, salinity and algal density and stores the data in CSV format.


    To understand this function better, the content structure of the types of files can be accessed by downloading the file and viewing it yourself.




    Returns
    -------

    **For '.asdf', '.hdf5' and '.zip' files:**
    
    data: np.ndarray
          Image data taken with the Lir, Manannan or Fand instrument for ASDF, HDF5 and ZIP files respectivley.
    meta_data: dict
               Other information about the data. This includes archive it's stored in, year, observatory, instrument, date when taken, time when taken, xcoords, ycoords, resolution. For ASDF files (ie Lir instrument data) the information about the asdf library is also included.




    **For '.csv' files:**
    
    turbulence: list
                300 turbulence measurements taken from the 300 deepest points in an area around the target region. 
    salinity: list
              300 salinity measurements taken from the 300 deepest points in an area around the target region. 
    algal_density: list
                   300 density measurements of algae taken from the 300 deepest points in an area around the target region. 
               
    
    
    
    """

    # Errors:
    if type(file) != str:
        raise TypeError("The file-name must be a string")

    if len(file.split('.')) != 2: # ensure it is a file 
        raise ValueError("The input must be a file. Not a folder or otherwise.")


    filetype = os.path.splitext(file)[1]  # obtain file extension

    if filetype != '.asdf' \
            and filetype != '.hdf5' \
            and filetype != '.zip':
        raise NameError("The file format is not supported. Only these are accepted: ASDF, HDF5 and ZIP.")


    if not Path(file).exists(): # if no such path/file exists
        raise FileNotFoundError("The input file does not exist.")



        

    filetype = os.path.splitext(file)[1] # obtain file extension

  
    if filetype == '.asdf':
        file = dict( asdf.open(file, 'r') )

        data = np.array(file['data'])

        del file['data']
        meta_data = file

        return data, meta_data



    elif filetype == '.hdf5':    
        f = h5py.File(file, 'r')

        data = f['observation']['data']
        meta_data = dict(f.attrs) | dict(f['observation'].attrs) # add the meta data together

        return data, meta_data



    elif filetype == '.zip':    
        with ZipFile(file) as myzip:

            file1 = myzip.namelist()[0]
            file2 = myzip.namelist()[1]



            # Just in case the files in the '.zip' are not sorted in alphabetical order,
            # extract the file extension, perform if statements for the file extension and
            # then load the files according to their respective extensions:

            filetype1 = os.path.splitext(file1)[1]
            filetype2 = os.path.splitext(file2)[1]




            myfile1 = myzip.read(file1)

            if filetype1 == '.npy':
                data = np.load(BytesIO(myfile1)) 
                # use io.BytesIO to help load the file (which includes bytes) in memory

            elif filetype1 == '.json':
                meta_data = json.load(BytesIO(myfile1))




            myfile2 = myzip.read(file2)

            if filetype2 == '.npy':
                data = np.load(BytesIO(myfile2))
            elif filetype2 == '.json':
                meta_data = json.load(BytesIO(myfile2))




            return np.array(data), dict(meta_data)

            


    elif filetype == '.csv':
        with open(file) as mycsv:
            csvfile = csv.reader(mycsv, delimiter=',')

            turbulence = []
            salinity = []
            algal_density = []
            
            for row in csvfile:
                turbulence.append(row[0])
                salinity.append(row[1])
                algal_density.append(row[2])

            return turbulence, salinity, algal_density