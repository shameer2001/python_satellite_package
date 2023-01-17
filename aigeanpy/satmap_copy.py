from ctypes import Union
from pathlib import Path
from read_copy import *

class SatMap:
    """
    
    
    """

    def __init__(self, file):
        self.file = file
        
        # Raise Error:
        filetype = os.path.splitext(self.file)[1] # obtain file extension

        if filetype != '.asdf' \
            and filetype != '.hdf5' \
                and filetype != '.zip' \
                    and filetype != '.csv':

                raise NameError("")



    # def mosaic(self, otherMap: 'SatMap', resolution: int, padding: bool) -> 'SatMap':
    #     # todo: allow to combine images as when using + but allowing mixing instruments (with different resolution!).
    #     ...

    # def visualise(self, save: bool, savepath:Union(Path, str), **kwargs) -> None:
    #     # todo: Show the axis as in earth coordinates and with the proper orientation of the image.
    #     ...

    # todo: Also need to support the + and - operation



    def meta(self):
        """Extracts meta data from the input file.
        Parameters
        ----------
        self: str
              The name of the file or path to the file. 
        Returns
        -------
        meta_data: dict
                   Other information about the data including the archive, year, observatory, instrument, date when taken, time when taken, xcoords, ycoords and resolution.
        """
        meta_data = read(self.file)[1] 
        
        return meta_data

    def data(self):
        """Extracts data from the input file.
        Parameters
        ----------
        self: str
              The name of the file or path to the file. 
        Returns
        -------
        data: ndarray
              Image data taken with the respective instrument.
        """
        data=read(self.file)[0]

        return data


    def shape(self):
        """The shape of the data from the imager instrument.
        Parameters
        ----------
        self: ndarray
              Image data taken with the instrument.
        Returns
        -------
        shape: tuple
              Shape of the data.
        """

        return np.shape(self.data())



    def fov(self):
        """Field of view of the images captured by the instrument (i.e., the difference between the boundaries).
        
        Parameters
        ----------
        self: dict
              Meta data of the measurements taken by the instrument.
        Returns
        -------
        fov: tuple
              The range of x-coordinates and range of y-coordinates (i.e the field of view).
        """


        x_min_max, y_min_max = self.meta()['xcoords'], self.meta()['ycoords']
        fov = (x_min_max[1] - x_min_max[0], y_min_max[1] - y_min_max[0])

        return fov



    def centre(self):
        """Centre of the image taken by the instrument.
        
        Parameters
        ----------
        self: dict
              Meta data of the measurements taken by the instrument.
        Returns
        -------
        centre: tuple
              Coordinates of the centre of the image.
        """

        x_min_max, y_min_max = self.meta()['xcoords'], self.meta()['ycoords']

        centre = (    (x_min_max[1] + x_min_max[0])/2  ,   (y_min_max[1] - y_min_max[0])/2  )

        return centre







# satmap = SatMap("aigean_man_20221205_194510.hdf5")
# satmap = SatMap("aigean_lir_20221205_191610.asdf")
# print(satmap.data(),'data')

# print(satmap.meta(),'meta')
# print(satmap.data())
# print(satmap.meta())
# print(type(satmap.shape()))
# print(type(satmap.fov()))
# print(satmap.fov())
#print(pixel_to_earth("aigean_lir_20221205_191610.asdf", satmap.data()[0]))




# def get_satmap(file_name) -> 'SatMap':
#     # todo: Give the name of the file, and return the data and meta,
#     #  where data gives the array, meta gives a dictionary with the metadata of the file.
#     ...
#     satmap = SatMap(file_name)
#     data = satmap.data()
#     meta = satmap.meta()
#     return data, meta 

