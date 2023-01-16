from net import *
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
    
    Each of the instruments used different file formats to store the data and meta data:

    Lir uses Advanced Scientific Data Format (ASDF). File extension: '.asdf'   
    Manannn uses Hierarchical Data Format 5 (HDF5). 
    Fand stores the data in 'npy' format and the meta data in JSON files
    Ecne measures turbulence, salinity and algal density and stores the data in CSV format



    To understand this function better, the content structure of the types of files are detailed below:

    The structure of the '.asdf' files:

    root (asdf object)
    ├─asdf_library (Software)
    │ ├─author (str): The ASDF Developers
    │ ├─homepage (str): http://github.com/asdf-format/asdf
    │ ├─name (str): asdf
    │ └─version (str): 2.14.2
    ├─history (dict)
    │ └─extensions (list)
    │   └─[0] (ExtensionMetadata) ...
    ├─archive (str): ISA
    ├─data (NDArrayType): shape=(val, val), dtype=float64   
    ├─date (str): YYYY-mm-dd
    ├─instrument (str): Lir
    ├─observatory (str): Aigean
    ├─resolution (int): 30
    ├─time (str): hh:mm:ss
    ├─xcoords (list)
    │ ├─[0] (float): val
    │ └─[1] (float): val
    ├─ycoords (list)
    │ ├─[0] (float): val
    │ └─[1] (float): val
    └─year (int): YYYY



    The structure of the '.hdf5' files:

    root (hdf5 object)
    |─attrs:
      |─archive (str) = 'ISA'
      |─year (int) = YYYY
    observation
    |─ attrs:
       |─date (str): 'YYYY-mm-dd'
       |─instrument (str): 'Manannan'
       |─observatory (str): 'Aigean'
       |─resolution (int): 15
       |─time (str); 'hh:mm:ss'
       |─xcoords (arr) 
         ├─[0] (float): val
         └─[1] (float): val
       |─ycoords (arr)
         ├─[0] (float): val
         └─[1] (float): val
    |─data (NDArrayType): float64(val x val)

    
    The structure of the '.json' files:
    
    dictionary 
    |─archive (str): "ISA"
    |─year (int): YYYY
    |─observatory (str): "Aigean"
    |─instrument (str): "Fand"
    |─date (str): "YYYY-mm-dd"
    |─time (str): "hh-mm-ss"
    |─xcoords (list) 
      ├─[0] (float): val
      └─[1] (float): val
    |─ycoords (list)
      ├─[0] (float): val
      └─[1] (float): val
    |─resolution (int): 5


    The structure of the '.npy' files:

    Array (NDArrayType)
    |─shape=(val, val), dtype=float64 



    The structure of the '.csv' files:
    
    Shape: 300 rows, 3 columns
    Columns: turbulence, salinity, algal density



    Returns
    -------

    For '.asdf', '.hdf5' and '.zip' files:

    data: ndarray
          Image data taken with the Lir, Manannan or Fand instrument for ASDF, HDF5 and ZIP files respectivley.
    meta_data: dict
               Other information about the data. This includes archive it's stored in, year, observatory, instrument, date when taken, time when taken, xcoords, ycoords, resolution. For ASDF files (ie Lir instrument data) the information about the asdf library is also included


    For '.csv' files:

    turbulence: list
                300 turbulence measurements taken from the 300 deepest points in an area around the target region. 
    salinity: list
              300 salinity measurements taken from the 300 deepest points in an area around the target region. 
    algal_density: list
                   300 density measurements of algae taken from the 300 deepest points in an area around the target region. 

               
    


    
    
    """

    # Errors:
    if type(file) != str:
        raise TypeError("")

    if not Path(file).exists(): # if no such path/file exists
        raise FileNotFoundError("")



        

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




# with asdf.open("aigean_lir_20221205_191610.asdf", 'r') as af:
#     print(af['xcoords'])

# #read("aigean_lir_20221205_191610.asdf") 

# payload = {'filename':"aigean_lir_20221205_191610.asdf"}
# r = get('https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/download/', params=payload)

# show_green_in_png(r.content)

#print( net.query_isa("2022-12-05", "2022-12-06", "fand") )
net.download_isa('aigean_fan_20221206_190424.zip')

myzipp = ZipFile('aigean_fan_20221206_190424.zip', 'r')

jsonn = myzipp.namelist()[0]

npyy = myzipp.namelist()[1]


lol = myzipp.open(npyy)
    #print(type(mynpyy))
    #BytesIO(mynpyy)
npyyy = np.load(lol)
#print(npyyy)


lol = myzipp.read(npyy)
    #print(type(mynpyy))
    #BytesIO(mynpyy)
npyyy = np.load(BytesIO(lol))
#print(npyyy)






lol2 = myzipp.read(jsonn)
    #print(type(mynpyy))
    #BytesIO(mynpyy)
jsonnn = json.load(BytesIO(lol2))
#print(jsonnn)


#lol2 = myzipp.open(jsonn)
    #print(type(mynpyy))
    #BytesIO(mynpyy)
#jsonnn = json.load(lol2)
#print(jsonnn)


#print( net.query_isa("2022-12-05", "2022-12-06", "ecne") )
net.download_isa('aigean_ecn_20221205_191610.csv')



# with open('aigean_ecn_20221205_191610.csv') as mycsv:
#     csvv = csv.reader(mycsv, delimiter=',')

#     turbulence = []
#     salinity = []
#     algal_density = []

#     for row in csvv:
#         turbulence.append(row[0])
#         salinity.append(row[1])
#         algal_density.append(row[2])

#     print(turbulence)

#print(net.query_isa("2022-12-05", "2022-12-06", "manannan") )
net.download_isa('aigean_man_20221206_181924.hdf5')

f = h5py.File('aigean_man_20221206_181924.hdf5', 'r')
#print(type(f.attrs))

# for i in f:
#     print(i)

#file = asdf.open('aigean_lir_20221205_191610.asdf', 'r') 
#print(type(file))


import nexusformat.nexus as nx
# f = nx.nxload('.h5py')
# print(f.tree)



jsonnn = json.load(BytesIO(lol2))
# for i in jsonnn:
#     print(i)

# print(type(read('aigean_lir_20221205_191610.asdf')[0]))
# print(type(read('aigean_lir_20221205_191610.asdf')[1]))



# print(type(read('aigean_man_20221206_181924.hdf5')[0]))
# print(type(read('aigean_man_20221206_181924.hdf5')[1]))




# print(type(read('aigean_fan_20221206_190424.zip')[0]))
# print(type(read('aigean_fan_20221206_190424.zip')[1]))



# print(type(read('aigean_ecn_20221205_191610.csv')[0]))
# print(type(read('aigean_ecn_20221205_191610.csv')[1]))
# print(type(read('aigean_ecn_20221205_191610.csv')[2]))
