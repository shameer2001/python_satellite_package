
import numpy as np


def earth_to_pixel(earth_coord: 'np.ndarray', meta: 'dict', resolution: float = None) -> np.array:
    """convert image to the pixel coord from earth coord

    Parameters
    ----------
    earth_coord: Numpy.array
           the image under the earth coord

    meta: dict
          Other information about the data including the archive, year, observatory, instrument, date when taken, time
          when taken, xcoords, ycoords and resolution.

    resolution: float, optional
          if provided, use this as the resolution, otherwise use the resolution provided in the meta (used in the
          SatMap.mosaic func, where user can specify the resolution)

    Notes
    -----
    In the case when the earth coordinate falls in the centre of multiple pixels, give the top-left corner

    Returns
    -------
    result: Numpy.array
            the image under the pixel coord

    >>> from aigeanpy.satmap import get_satmap
    >>> from aigeanpy.net import download_isa
    >>> download_isa("aigean_lir_20221205_191610.asdf")
    >>> satmap = get_satmap("aigean_lir_20221205_191610.asdf")
    >>> dict = pixel_to_earth(satmap.data, satmap.meta)
    >>> earthCoord = dict.get('earthCoord')
    >>> centralCoord = dict.get('centralCoord')
    >>> predictedPixel = earth_to_pixel(earthCoord, satmap.meta)
    >>> print(predictedPixel.shape)
    (10, 20)
    """

    # error raising: query using wrong data format
    if type(earth_coord) != np.ndarray:
        raise TypeError("The attribute earth_coord must be an numpy array.")

    if type(meta) != dict:
        raise TypeError("The attribute meta must be a dict.")

    if resolution and type(resolution) != float:
        raise TypeError("The attribute resolution must be a float number.")

    # convert earth coordinates to pixels, provide the top-right corner of the earth coordinate

    # get the resolution setting
    resolution = float(meta['resolution']) if resolution is None else float(resolution)

    # get the shape of the given earth data
    earthX, earthY = len(earth_coord[0]), len(earth_coord)

    # calculate the shape of pixel coord
    pixelX, pixelY = int(earthX/resolution), int(earthY/resolution)

    # create the array to store the pixel coord
    pixel = np.zeros((pixelY, pixelX))

    if resolution >= 1:
        # case that 1 pixel mapping to a resolution-by-resolution earth sub-array
        y = 0
        resolution = int(resolution)
        for i in range(pixelY):
            x = 0
            for j in range(pixelX):
                pixel[i][j] = earth_coord[y][x]
                x += resolution
            y += resolution
    else:
        # case that 1 earth mapping to a (1/resolution)-by-(1/resolution) earth sub-array
        step = int(1/resolution)
        y = 0
        for i in range(earthY):
            x = 0
            for j in range(earthX):
                pixel[y:y+step, x:x+step] = earth_coord[i][j]
                x += step
            y += step

    return pixel


def pixel_to_earth(pixel_coord: 'np.array', meta, resolution=None) -> dict:
    """convert image to the earth coord from pixel coord

    Parameters
    ----------
    pixel_coord: Numpy.array
           the image under the pixel coord

    meta: dict
          Other information about the data including the archive, year, observatory, instrument, date when taken, time
          when taken, xcoords, ycoords and resolution.

    resolution: float, optional
          if provided, use this as the resolution, otherwise use the resolution provided in the meta (used in the
          SatMap.mosaic func, where user can specify the resolution)

    Notes
    -----
    In the case when the earth coordinate falls in the centre of multiple pixels, give the top-left corner;

    Depending on the resolution of the image, a pixel may correspond to multiple earth coordinates. In such cases,
    pixel_to_earth should provide the coordinate of the centre of the pixel.


    Returns
    -------
    result: dict
            'earthCoord' gives the image under the earth pixel
            'centralCoord' gives the cenre of the pixel when a pixel correspond to multiple earth coordinates, otherwise
            is None

        >>> from aigeanpy.satmap import get_satmap
        >>> from aigeanpy.net import download_isa
        >>> download_isa("aigean_lir_20221205_191610.asdf")
        >>> satmap = get_satmap("aigean_lir_20221205_191610.asdf")
        >>> dict = pixel_to_earth(satmap.data, satmap.meta)
        >>> earthCoord = dict.get('earthCoord')
        >>> centralCoord = dict.get('centralCoord')
        >>> print(earthCoord.shape)
        (300, 600)
        >>> print(centralCoord.shape)
        (10, 20, 2)
    """
    # error raising: query using wrong data format

    if type(meta) != dict:
        raise TypeError("The attribute meta must be a dict.")

    if resolution and type(resolution) != float:
        raise TypeError("The attribute resolution must be a float number.")

    # convert pixels to earth coordinates, provide the coordinate of the centre of the pixel.

    # get the resolution setting
    resolution = float(meta['resolution']) if resolution is None else float(resolution)

    # get the shape of the given pixel data
    xcoords = list(meta['xcoords'])
    ycoords = list(meta['ycoords'])
    pixelX, pixelY = [int((xcoords[1] - xcoords[0]) / resolution), int((ycoords[1] - ycoords[0]) / resolution)]

    # calculate the shape of the earth coord
    earthX, earthY = int(pixelX * resolution), int(pixelY * resolution)

    # create the array to store the earth coord
    earth = np.zeros((earthY, earthX))

    if resolution >= 1:
        # case that 1 pixel mapping to a resolution-by-resolution earth sub-array
        y = 0
        resolution = int(resolution)
        for i in range(pixelY):
            x = 0
            for j in range(pixelX):
                earth[y:y+resolution, x:x+resolution] = pixel_coord[i][j]
                x += resolution
            y += resolution
    else:
        # case that 1 earth mapping to a (1/resolution)-by-(1/resolution) earth sub-array
        step = int(1/resolution)
        y = 0
        for i in range(earthY):
            x = 0
            for j in range(earthX):
                earth[i][j] = pixel_coord[y][x]
                x += step
            y += step

    # create the numpy array to store the central earth coord for each pixel if resolution >= 1
    central = [[0 for i in range(pixelX)] for j in range(pixelY)]

    if resolution >= 1:
        # if 1 pixel mapping multiple earth coord, provide the coordinate of centre of the pixel
        y = int(ycoords[0] + resolution/2)
        for i in range(pixelY):
            x = int(xcoords[0] + resolution/2)
            for j in range(pixelX):
                central[i][j] = [x, y]
                x += int(resolution)
            y += int(resolution)

    return {'earthCoord': np.array(earth), 'centralCoord': None if central is None else np.array(central)}






