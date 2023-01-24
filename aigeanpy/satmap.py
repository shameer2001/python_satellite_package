from typing import Union
from pathlib import Path

from utils import earth_to_pixel, pixel_to_earth

import numpy as np
from datetime import datetime
from skimage.transform import rescale, downscale_local_mean, resize
import os
import matplotlib.pyplot as plt
import json
from net import *

#from aigeanpy.read import *
from read import *




class SatMap:
    """
    Obtains data, meta-data, properties and also manipulates the image(s).
    

    Attributes
    ----------
    meta: dict
          Other information about the data of the input file. This includes archive it is stored in, year observatory, instrument, date when taken, time when taken, xcoords, ycoords, resolution. For ASDF file (ie Lir instrument data) the information about the asdf library is also included.
    data: ndarray
          Image datal (from the input file) taken with the Lir, Manannan or Fand instrument for ASDF, HDF5 and ZIP files respectivley.
    shape: tuple
           Shape of the data of the input file.
    fov: tuple
         The range of x-coordinates and range of y-coordinates (i.e the field of view).
    centre: tuple
            Coordinates of the centre of the image in the input file.
    



    Methods
    -------
    __add__(other: 'SatMap')
           Collate two images and create the new SatMap instance

    __sub__(other: 'SatMap')
           Obtain a difference image to measure change between the days, which will only work
           when the data is overlapping.
    
    mosaic (other: 'SatMap', resolution: int = None, padding: bool = True)
          Combine images as when using + but allowing mixing instruments with different resolution
    
    visualise (save: bool = False, savepath: Union[Path, str] = os.getcwd())
            Visualise the image, show the axis as in earth coordinates and with the proper orientation of the image.




    """

    def __init__(self, meta, data, shape, fov, centre):
        self.meta = meta
        self.data = data
        self.shape = shape
        self.fov = fov
        self.centre = centre


    # support the + and - operation
    def __add__(self, other: 'SatMap'):
        """self defined + operation, collate two images and create the new SatMap instance (i.e, if we got an image
            covering the (0,0)-(10,10) range and another from (12, 5)-(22,15), then we would end up with a “canvas”
            that goes from (0,0)-(22,15).)

        Parameters
        ----------
        other: SatMap
               Another image to be added to the current image

        Notes
        -----
        When the two images are overlapping, the values of the overlapping areas should not be added. Otherwise
        it would give the wrong impression. Values should be the same when observed the same day.

        Returns
        -------
        result: SatMap
                the image created by the addition of two input images

        Examples
        --------
        >>> from aigeanpy.satmap import get_satmap
        >>> from aigeanpy.net import download_isa
        >>> download_isa("aigean_lir_20221205_191610.asdf")
        >>> download_isa("aigean_lir_20221205_194510.asdf")
        >>> satmap1 = get_satmap("aigean_lir_20221205_191610.asdf")
        >>> satmap2 = get_satmap("aigean_lir_20221205_194510.asdf")
        >>> combine = satmap1 + satmap2
        >>> combine.shape
        (13, 30)
        >>> combine.fov
        (900.0, 400.0)
        >>> combine.centre
        (950.0, 300.0)
        """

        # error raising: query using wrong data format
        if type(other) != SatMap:
            raise TypeError("The attribute other must be a SatMap instance.")

        # check if the two images can be added or not
        if self.meta['date'] != other.meta['date']:
            raise TypeError("only the images from the same day can be added")

        if self.meta['instrument'] != other.meta['instrument']:
            raise TypeError("only the images from the same instrument can be added")

        # convert both of two image pixel data into earth coord
        earthA = pixel_to_earth(self.data, self.meta)
        earthB = pixel_to_earth(other.data, other.meta)

        coordA = earthA['earthCoord']
        coordB = earthB['earthCoord']

        # specify the boundary of final combined result (top-left, bottom-right)
        xLowA, xHighA = self.meta['xcoords']
        yLowA, yHighA = self.meta['ycoords']

        xLowB, xHighB = other.meta['xcoords']
        yLowB, yHighB = other.meta['ycoords']

        xLow, xHigh = min(xLowA, xLowB), max(xHighA, xHighB)
        yLow, yHigh = min(yLowA, yLowB), max(yHighA, yHighB)

        # do the add logic
        data = np.zeros((int(yHigh - yLow), int(xHigh - xLow)))
        data[int(yLowA-yLow):int(yHighA-yLow), int(xLowA-xLow):int(xHighA-xLow)] = coordA
        data[int(yLowB-yLow):int(yHighB-yLow), int(xLowB-xLow):int(xHighB-xLow)] = coordB
        data = earth_to_pixel(data, self.meta)

        # create the new SatMap instance to store the result
        shape = data.shape
        fov = (xHigh - xLow, yHigh - yLow)
        centre = ((xHigh+xLow)/2, (yHigh+yLow)/2)

        now = datetime.now()

        meta = dict()
        meta['archive'] = self.meta['archive']
        meta['year'] = now.year
        meta['observatory'] = self.meta['observatory']
        meta['instrument'] = self.meta['instrument']
        meta['date'] = now.date()
        meta['time'] = now.time()
        meta['xcoords'] = [xLow, xHigh]
        meta['ycoords'] = [yLow, yHigh]
        meta['resolution'] = self.meta['resolution']
        # add the extra property, indicating the source of the image (add/subtract/mosaic/origin)
        meta['source'] = "add"

        # return the new SatMap instance
        return SatMap(meta, data, shape, fov, centre)

    def __sub__(self, other: 'SatMap'):
        """self defined - operation, obtain a difference image to measure change between the days, which will only work
            when the data is overlapping. (i.e, if we have taken an image yesterday covering (0,0)-(10,10), and today
            another in the range of (5, 5)-(15, 15), the resultant image should be the difference between the both for
            the range (5, 5)-(10, 10).)

        Parameters
        ----------
        other: SatMap
               Another image to be subtracted from the current image

        Notes
        -----
        Two images must be taken from different days. And they must overlap with each other

        Returns
        -------
        result: SatMap
                the image created by the subtraction of two input images

        Examples
        --------
        >>> from aigeanpy.satmap import get_satmap
        >>> from aigeanpy.net import download_isa
        >>> download_isa("aigean_lir_20221205_191610.asdf")
        >>> download_isa("aigean_lir_20221207_175138.asdf")
        >>> satmap1 = get_satmap("aigean_lir_20221205_191610.asdf")
        >>> satmap2 = get_satmap("aigean_lir_20221207_175138.asdf")
        >>> combine = satmap1 - satmap2
        >>> combine.shape
        (10, 16)
        >>> combine.fov
        (700.0, 300.0)
        >>> combine.centre
        (750.0, 350.0)
        """

        # error raising: query using wrong data format
        if type(other) != SatMap:
            raise TypeError("The attribute other must be a SatMap instance.")

        # check if the two images can be added or not
        if self.meta['date'] == other.meta['date']:
            raise TypeError("only the images from two different days can be subtracted")

        if self.meta['instrument'] != other.meta['instrument']:
            raise TypeError("only the images from the same instrument can be subtracted")

        xLowA, xHighA = self.meta['xcoords']
        yLowA, yHighA = self.meta['ycoords']

        xLowB, xHighB = other.meta['xcoords']
        yLowB, yHighB = other.meta['ycoords']

        xDist = abs(xLowA - xLowB)
        yDist = abs(yLowA - yLowB)

        maxX = max(abs(xHighB-xLowB), abs(xHighA-xLowA))
        maxY = max(abs(yHighB-yLowB), abs(yHighA-yLowA))

        if yDist >= maxY or xDist >= maxX:
            raise TypeError("two images can not be subtracted because they have no overlap")

        # convert both of two image pixel data into earth coord
        earthA = pixel_to_earth(self.data, self.meta)
        earthB = pixel_to_earth(other.data, other.meta)

        coordA = earthA['earthCoord']
        coordB = earthB['earthCoord']

        # specify the boundary of final combined result (top-left, bottom-right)
        xLow, xHigh = min(xLowA, xLowB), max(xHighA, xHighB)
        yLow, yHigh = min(yLowA, yLowB), max(yHighA, yHighB)

        # do the add logic
        dataA = np.zeros((int(yHigh - yLow), int(xHigh - xLow)))
        dataB = np.zeros((int(yHigh - yLow), int(xHigh - xLow)))
        dataA[int(yLowA-yLow):int(yHighA-yLow), int(xLowA-xLow):int(xHighA-xLow)] = coordA
        dataB[int(yLowB-yLow):int(yHighB-yLow), int(xLowB-xLow):int(xHighB-xLow)] = coordB
        data = dataA-dataB
        finalData = data[int(max(yLowA-yLow, yLowB-yLow)):int(min(yHighA-yLow, yHighB-yLow)), int(max(xLowA-xLow, xLowB-xLow)):int(min(xHighA-xLow, xHighB-xLow))]

        finalData = earth_to_pixel(finalData, self.meta)

        # create the new SatMap instance to store the result
        shape = finalData.shape
        fov = (xHigh - xLow, yHigh - yLow)
        centre = ((xHigh+xLow)/2, (yHigh+yLow)/2)

        now = datetime.now()

        meta = dict()
        meta['archive'] = self.meta['archive']
        meta['year'] = now.year
        meta['observatory'] = self.meta['observatory']
        meta['instrument'] = self.meta['instrument']
        meta['date'] = now.date()
        meta['time'] = now.time()
        meta['xcoords'] = [max(xLowA, xLowB), min(xHighA, xHighB)]
        meta['ycoords'] = [max(yLowA, yLowB), min(yHighA, yHighB)]
        meta['resolution'] = self.meta['resolution']
        # add the extra property, indicating the source of the image (add/subtract/mosaic/origin)
        meta['source'] = "subtract"

        # return the new SatMap instance
        return SatMap(meta, data, shape, fov, centre)

    def mosaic(self, other: 'SatMap', resolution: int = None, padding: bool = True) -> 'SatMap':
        """allow to combine images as when using + but allowing mixing instruments with different resolution

        Parameters
        ----------
        other: SatMap
               Another image which do the mosaic operation with current image

        resolution: int, optional
                    If the resolution is not provided it should use the one of the two satmaps with larger detail, and
                    expand the other to that level.

        padding: bool, optional
                 padding should be True by default, i.e., to return an image with blanks (NaNs) on it. However, if
                 padding is set as False the resultant image should only cover maximum portion without blanks on the
                 image. Besides, if padding is False, then two images must overlap with each other

        Returns
        -------
        result: SatMap
                the image created by doing the mosaic operation on two input images
        """

        # error raising: query using wrong data format
        if type(other) != SatMap:
            raise TypeError("The attribute other must be a SatMap instance.")

        if resolution and type(resolution) != int:
            raise TypeError("The attribute resolution must be an integer.")

        if padding and type(padding) != bool:
            raise TypeError("The attribute padding must be a boolean value.")

        # allow to combine images as when using + but allowing mixing instruments (with different resolution!).

        # check if the two images can be added or not
        if self.meta['date'] != other.meta['date']:
            raise Exception("only the images from the same day can be added")

        # get the rescale factor for both images
        resolution = float(resolution) if resolution is not None else max(float(self.meta['resolution']), float(other.meta['resolution']))
        factorA = self.meta['resolution'] / resolution
        factorB = other.meta['resolution'] / resolution

        # rescale the pixelA and pixelB, to uniform their resolution
        pixelA = rescale(self.data, factorA) if factorA <= 1 else downscale_local_mean(self.data, (factorA, factorA))
        pixelB = rescale(other.data, factorB) if factorB <= 1 else downscale_local_mean(other.data, (factorB, factorB))

        # then execute the identical logic as the + operation
        # convert both of two image pixel data into earth coord
        earthA = pixel_to_earth(pixelA, self.meta, resolution)
        earthB = pixel_to_earth(pixelB, other.meta, resolution)

        # todo Note that changes in resolution may necessitate changes in field-of-view.
        #  In this case, your code should raise an appropriate exception (NOT SURE HOW TO DO)

        coordA = earthA['earthCoord']
        coordB = earthB['earthCoord']

        # specify the boundary of final combined result (top-left, bottom-right)
        xLowA, xHighA = self.meta['xcoords']
        yLowA, yHighA = self.meta['ycoords']

        xLowB, xHighB = other.meta['xcoords']
        yLowB, yHighB = other.meta['ycoords']

        if not padding:
            xDist = abs(xLowA - xLowB)
            yDist = abs(yLowA - yLowB)

            maxX = max(abs(xHighB-xLowB), abs(xHighA-xLowA))
            maxY = max(abs(yHighB-yLowB), abs(yHighA-yLowA))

            if yDist >= maxY or xDist >= maxX:
                raise Exception("cannot perform mosaic without padding on these two images because they have no overlap")

        # the xcoord and ycoord choice differs depending on the padding
        if not padding:
            xLow, xHigh = min(xLowA, xLowB), max(xHighA, xHighB)
            yLow, yHigh = max(yLowA, yLowB), min(yHighA, yHighB)
        else:
            xLow, xHigh = min(xLowA, xLowB), max(xHighA, xHighB)
            yLow, yHigh = min(yLowA, yLowB), max(yHighA, yHighB)

        # do the add logic
        data = np.zeros((int(yHigh - yLow), int(xHigh - xLow)))
        data[int(yLowA-yLow):int(yHighA-yLow), int(xLowA-xLow):int(xHighA-xLow)] = coordA
        data[int(yLowB-yLow):int(yHighB-yLow), int(xLowB-xLow):int(xHighB-xLow)] = coordB
        data = earth_to_pixel(data, self.meta)

        # create the new SatMap instance to store the result
        shape = data.shape
        fov = (xHigh - xLow, yHigh - yLow)
        centre = ((xHigh+xLow)/2, (yHigh+yLow)/2)

        now = datetime.now()

        meta = dict()
        meta['archive'] = self.meta['archive']
        meta['year'] = now.year
        meta['observatory'] = self.meta['observatory']
        meta['instrument'] = self.meta['instrument'] + ' + ' + other.meta['instrument']
        meta['date'] = now.date()
        meta['time'] = now.time()
        meta['xcoords'] = [xLow, xHigh]
        meta['ycoords'] = [yLow, yHigh]
        meta['resolution'] = resolution
        # add the extra property, indicating the source of the image (add/subtract/mosaic/origin)
        meta['source'] = "mosaic"

        # return the new SatMap instance
        return SatMap(meta, data, shape, fov, centre)

    def visualise(self, save: bool = False, savepath: Union[Path, str] = os.getcwd(), **kwargs):
        """ visualise the image, show the axis as in earth coordinates and with the proper orientation of the image.

        Parameters
        ----------
        save: bool, optional
               If save is set to True, then the image should not be displayed on the screen and saved in the required
               path

        savepath: Union[Path, str], optional
                the required saved path, if not set, the savepath will be the current directory


        Notes
        -----
        the saved image is titled with the following pattern: {observatory}_{instrument}_{date}_{time}{_source}.png,
        where the date and time are formatted as YYYYmmdd (e.g., 20221231) and HHMMSS (e.g., 120034) respectively, the
        source has four different values: add/subtract/mosaic/origin, each indicate how that image is generated.
        """

        # error raising: query using wrong data format
        if save and type(save) != bool:
            raise TypeError("The attribute save must be a boolean value.")

        if savepath and type(savepath) != str and type(savepath) != Path:
            raise TypeError("The attribute savepath must be either a string or a Path instance.")

        # Show the axis as in earth coordinates and with the proper orientation of the image.

        # get the self.data as the pixel coord, and convert it to earth coord
        earth = pixel_to_earth(self.data, self.meta)
        earthArray = earth['earthCoord']

        xLow, xHigh = list(self.meta['xcoords'])
        yLow, yHigh = list(self.meta['ycoords'])

        resolution = int(self.meta['resolution'])

        xDist = xHigh - xLow
        yDist = yHigh - yLow

        fig = plt.figure(figsize=(xDist/(1.2*resolution), yDist/(1.2*resolution)))
        plt.imshow(earthArray, cmap='Blues', origin='lower')
        plt.colorbar()
        plt.yticks(np.arange(0, yHigh - yLow, resolution), np.arange(yLow, yHigh, resolution))
        plt.xticks(np.arange(0, xHigh - xLow, resolution), np.arange(xLow, xHigh, resolution), rotation=270)

        if save:
            # if save=True, save the graph:
            observatory = str(self.meta['observatory'])
            instrument = str(self.meta['instrument'])
            source = str(self.meta.get("source", "origin"))
            date = "".join(str(self.meta['date']).split('-'))

            time = str(self.meta['time'])
            time = time[:8] if len(time) >= 8 else time
            time = "".join(time.split(":"))

            title = "_".join([observatory, instrument, date, time, source])

            path = os.path.join(savepath, title)
            plt.savefig(path)
        else:
            # otherwise, show the graph
            plt.show()


def get_satmap(file_name) -> 'SatMap':
    """Generates a `SatMap` class object for a given file.

    Parameter
    ---------
    file_name: str
               The name of the file that the function will return a SatMap object of.

    Returns
    -------
    satmap: 'SatMap'
             A SatMap class oject for the file named 'file_name'



    Example:
    --------

    >>> satmap = get_satmap("aigean_lir_20221205_191610.asdf")
    >>> satmap.meta
    {'asdf_library': {'author': 'The ASDF Developers', 'homepage': 'http://github.com/asdf-format/asdf', 'name': 'asdf', 'version': '2.14.2'}, 'history': {'extensions': [{'extension_class': 'asdf.extension.BuiltinExtension', 'software': {'name': 'asdf', 'version': '2.14.2'}}]}, 'archive': 'ISA', 'date': '2022-12-05', 'instrument': 'Lir', 'observatory': 'Aigean', 'resolution': 30, 'time': '19:16:10', 'xcoords': [500.0, 1100.0], 'ycoords': [200.0, 500.0], 'year': 2023}
    >>> satmap.shape
    (10, 20)
    >>> satmap.fov
    (600.0, 300.0)
    >>> satmap.centre
    (800.0, 150.0)
             
    """
    # Give the name of the file, and return the data and meta,
    #  where data gives the array, meta gives a dictionary with the metadata of the file.
    # Raise Error:

    # Errors:
    if type(file_name) != str:
        raise TypeError("The file-name must be a string")


    filetype = os.path.splitext(file_name)[1]  # obtain file extension

    if filetype != '.asdf' \
            and filetype != '.hdf5' \
            and filetype != '.zip':
        raise NameError("The file format is not supported. Only these are accepted: ASDF, HDF5 and ZIP.")


    if not Path(file_name).exists(): # if no such path/file exists
        raise FileNotFoundError("The input file does not exist.")






    
    # the attributes of the SatMap class:
    meta = read(file_name)[1]
    data = read(file_name)[0]
    shape = np.shape(data)
    theFov = fov(meta)
    theCentre = centre(meta)

    return SatMap(meta, data, shape, theFov, theCentre)


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

    # ERROR MESSAGE:
    # for i in query: assert (np.size(i['xcoords']) == 2 and np.size(i['ycoords']) == 2)  # test for shape of x and y coordinate range

    x_min_max, y_min_max = meta['xcoords'], meta['ycoords']

    centre = ((x_min_max[1] + x_min_max[0]) / 2, (y_min_max[1] - y_min_max[0]) / 2)

    return centre


# query = net.query_isa("2023-01-10", "2023-01-13", 'manannan')
# net.download_isa(query[0]['filename'])
# satmap = get_satmap(query[0]['filename'])
# #satmap = get_satmap("aigean_man_20221206_181924.hdf5")
# print(satmap.meta)
# print(satmap.shape)




# query = net.query_isa("2023-01-10", "2023-01-13", 'lir')
# net.download_isa(query[0]['filename'])
# satmap = get_satmap(query[0]['filename'])
# #satmap = get_satmap("aigean_lir_20221205_191610.asdf")
# print(satmap.meta)
# print(satmap.shape)




# query = net.query_isa("2023-01-10", "2023-01-13", 'fand')
# net.download_isa(query[0]['filename'])
# satmap = get_satmap(query[0]['filename'])
# #satmap = get_satmap("aigean_fan_20221206_190424.zip")
# print(satmap.meta)
# print(satmap.shape)

# print(satmap.data)
# print(satmap.shape)
# print(satmap.fov)
# print(satmap.centre)


# print(type(satmap.meta))
# print(type(satmap.data))
# print(type(satmap.shape))
# print(type(satmap.fov))
# print(type(satmap.centre))


#print(net.query_isa("2022-12-20", "2022-12-23", 'lir'))

#print(net.query_isa("2022-12-29", "2022-12-31", 'manannan'))
# if query == None:
#     print("ok")
#print(type(query))
#net.download_isa(query[0]['filename'])



# query = net.query_isa("2023-01-01", "2023-01-04", 'lir')
# #print(query)
# net.download_isa(query[0]['filename'])

# query = net.query_isa("2023-01-01", "2023-01-04", 'lir')
# #print(query)
# net.download_isa(query[0]['filename'])

# query = query_isa("2022-12-02", "2022-12-05", 'lir')
# download_isa(query[0]['filename'])
# satmap = get_satmap(query[0]['filename'])

#print(satmap.centre)


# query2 = net.query_isa("2022-12-02", "2022-12-05", 'lir')
# net.download_isa(query2[1]['filename'])
# satmap2 = get_satmap(query2[1]['filename'])

# mos_satmap = satmap.mosaic(other=satmap2)
# print(mos_satmap.data)

# # print(satmap.centre)

# download_isa("aigean_lir_20221205_191610.asdf")
# satmap = get_satmap("aigean_lir_20221205_191610.asdf")

# print(satmap.meta)
# print(satmap.shape)
# print(satmap.fov)
# print(satmap.centre)
#satmap = get_satmap("aigean_lir_20221205_191610.asdf").__add__(satmap).shape
#print(satmap)
# if __name__ == "__main__":
#     satmap1 = get_satmap("aigean_lir_20221205_191610.asdf")
#     satmap2 = get_satmap("aigean_lir_20221207_175138.asdf")
#     combine = satmap1 - satmap2
#     print(combine.shape)
#     print(combine.fov)
#     print(combine.centre)



