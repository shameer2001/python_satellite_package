from ctypes import Union
from pathlib import Path
from read import *

# FUNCTIONS FOR THE ATTRIBUTES OF THE SatMap function:


def fov(meta):
    """Field of view of the images captured by the instrument (i.e., the difference between the boundaries).
        
    Parameters
    ----------

    meta: dict
         Meta data of the measurements taken by the instrument.

        Returns
        -------
        fov: tuple
              The range of x-coordinates and range of y-coordinates (i.e the field of view).
    """


    x_min_max, y_min_max = meta['xcoords'], meta['ycoords']
    fov = (x_min_max[1] - x_min_max[0], y_min_max[1] - y_min_max[0])

    return fov



def centre(meta):
    """Centre of the image taken by the instrument.
        
        Parameters
        ----------

        meta: dict
              Meta data of the measurements taken by the instrument.

        Returns
        -------
        centre: tuple
              Coordinates of the centre of the image.
    """

    x_min_max, y_min_max = meta['xcoords'], meta['ycoords']

    centre = (    (x_min_max[1] + x_min_max[0])/2  ,   (y_min_max[1] - y_min_max[0])/2  )

    return centre









# THE SatMap CLASS:


class SatMap:
    """
    
    
    """

    def __init__(self, file):
        self.meta = read(file)[1] 
        self.data = read(file)[0] 
        self.shape = np.shape(self.data)
        self.fov = fov(self.meta)
        self.centre = centre(self.meta)

        
        # Raise Error:
        filetype = os.path.splitext(file)[1] # obtain file extension

        if filetype != '.asdf' \
            and filetype != '.hdf5' \
                and filetype != '.zip':

                raise NameError("The file format is not supported. Only these are accepted: ASDF, HDF5 and ZIP.")




    # def mosaic(self, otherMap: 'SatMap', resolution: int, padding: bool):
    # #     # todo: allow to combine images as when using + but allowing mixing instruments (with different resolution!).
    #     ...

    # def visualise(self, save: bool, savepath:Union(Path, str), **kwargs):
    # #     # todo: Show the axis as in earth coordinates and with the proper orientation of the image.
    #     ...

    # todo: Also need to support the + and - operation





def get_satmap(file_name) -> 'SatMap':
    # todo: Give the name of the file, and return the data and meta,
    #  where data gives the array, meta gives a dictionary with the metadata of the file.


    return SatMap(file_name)






satmap = get_satmap("aigean_man_20221206_181924.hdf5")
satmap = get_satmap("aigean_lir_20221205_191610.asdf")

#print(satmap.data())

#print(satmap.meta())
#print(satmap.data())
#print(satmap.meta())
# print(type(satmap.shape()))
# print(type(satmap.fov()))
# print(satmap.fov())

print(satmap.meta)
print(satmap.data)
print(satmap.shape)
print(satmap.fov)
print(satmap.centre)


print(type(satmap.meta))
print(type(satmap.data))
print(type(satmap.shape))
print(type(satmap.fov))
print(type(satmap.centre))
