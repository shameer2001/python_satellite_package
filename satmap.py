from ctypes import Union
from pathlib import Path
from aigeanpy.utils import earth_to_pixel, pixel_to_earth
import numpy as np
import datetime
from skimage.transform import rescale, downscale_local_mean


class SatMap:
    def __init__(self, meta, data, shape, fov, centre):
        self.meta = meta
        self.data = data
        self.shape = shape
        self.fov = fov
        self.centre = centre

    # support the + and - operation
    def __add__(self, other: 'SatMap'):
        # check if the two images can be added or not
        if self.meta['date'] != other.meta['date']:
            raise Exception("only the images from the same day can be added")

        if self.meta['instrument'] != other.meta['instrument']:
            raise Exception("only the images from the same instrument can be added")

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
        data = np.zeros((yHigh - yLow, xHigh - xLow))
        data[yLowA - yLow:yHighA - yHigh, xLowA - xLow:xHighA - xLow] = coordA
        data[yLowB - yLow:yHighB - yHigh, xLowB - xLow:xHighB - xLow] = coordB
        data = earth_to_pixel(data, self.meta)

        # create the new SatMap instance to store the result
        shape = data.shape
        fov = (xHigh - xLow, yHigh - yLow)
        centre = ((xHigh+xLow)/2, (yHigh+yLow)/2)

        now = datetime.datetime.now()

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

    def __sub__(self, other):
        # check if the two images can be added or not
        if self.meta['date'] == other.meta['date']:
            raise Exception("only the images from two different days can be subtracted")

        if self.meta['instrument'] != other.meta['instrument']:
            raise Exception("only the images from the same instrument can be subtracted")

        xLowA, xHighA = self.meta['xcoords']
        yLowA, yHighA = self.meta['ycoords']

        xLowB, xHighB = other.meta['xcoords']
        yLowB, yHighB = other.meta['ycoords']

        xDist = abs(xLowA - xLowB)
        yDist = abs(yLowA - yLowB)

        maxX = max(abs(xHighB-xLowB), abs(xHighA-xLowA))
        maxY = max(abs(yHighB-yLowB), abs(yHighA-yLowA))

        if yDist >= maxY or xDist >= maxX:
            raise Exception("two images can not be subtracted because they have no overlap")

        # convert both of two image pixel data into earth coord
        earthA = pixel_to_earth(self.data, self.meta)
        earthB = pixel_to_earth(other.data, other.meta)

        coordA = earthA['earthCoord']
        coordB = earthB['earthCoord']

        # specify the boundary of final combined result (top-left, bottom-right)
        xLow, xHigh = max(xLowA, xLowB), min(xHighA, xHighB)
        yLow, yHigh = max(yLowA, yLowB), min(yHighA, yHighB)

        # do the subtract logic
        data = coordA[xLow-xLowA:xHigh, yLow-yLowA:yHigh] - coordB[xLow-xLowB:xHigh, yLow-yLowB:yHigh]
        data = earth_to_pixel(data, self.meta)

        # create the new SatMap instance to store the result
        shape = data.shape
        fov = (xHigh - xLow, yHigh - yLow)
        centre = ((xHigh+xLow)/2, (yHigh+yLow)/2)

        now = datetime.datetime.now()

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
        meta['source'] = "subtract"

        # return the new SatMap instance
        return SatMap(meta, data, shape, fov, centre)

    def mosaic(self, other: 'SatMap', resolution=None, padding=True) -> 'SatMap':
        # allow to combine images as when using + but allowing mixing instruments (with different resolution!).

        # check if the two images can be added or not
        if self.meta['date'] != other.meta['date']:
            raise Exception("only the images from the same day can be added")

        # get the rescale factor for both images
        resolution = float(resolution) if not None else max(float(self.meta['resolution']), float(other.meta['resolution']))
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

        # the xcoord and ycoord choice differs depending on the padding
        if not padding:
            xLow, xHigh = min(xLowA, xLowB), max(xHighA, xHighB)
            yLow, yHigh = max(yLowA, yLowB), min(yHighA, yHighB)
        else:
            xLow, xHigh = min(xLowA, xLowB), max(xHighA, xHighB)
            yLow, yHigh = min(yLowA, yLowB), max(yHighA, yHighB)

        # do the add logic
        data = np.zeros((yHigh - yLow, xHigh - xLow))
        data[yLowA - yLow:yHighA - yHigh, xLowA - xLow:xHighA - xLow] = coordA
        data[yLowB - yLow:yHighB - yHigh, xLowB - xLow:xHighB - xLow] = coordB
        data = earth_to_pixel(data, self.meta, resolution)

        # create the new SatMap instance to store the result
        shape = data.shape
        fov = (xHigh - xLow, yHigh - yLow)
        centre = ((xHigh+xLow)/2, (yHigh+yLow)/2)

        now = datetime.datetime.now()

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

    def visualise(self, save: bool, savepath:Union(Path, str), **kwargs) -> None:
        # todo: Show the axis as in earth coordinates and with the proper orientation of the image.
        ...


def get_satmap(file_name) -> 'SatMap':
    # todo: Give the name of the file, and return the data and meta,
    #  where data gives the array, meta gives a dictionary with the metadata of the file.
    ...


