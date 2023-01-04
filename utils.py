
import numpy as np
import json


def earth_to_pixel(earth_coord, meta):
    # todo: convert earth coordinates to pixels, provide the top-right corner of the earth coordinate
    ...


def pixel_to_earth(pixel_coord, meta):
    # convert pixels to earth coordinates, provide the coordinate of the centre of the pixel.

    # get the resolution setting
    resolution = float(meta['resolution'])

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


if __name__ == "__main__":
    earth = np.zeros((10, 10))
    earth[0:5, 0:5] = 1
    print(earth)

    pixel = np.load('observation.npy')
    f = open('metadata.json')
    meta = json.load(f)
    print(meta['resolution'])

    predictedEarth = pixel_to_earth(pixel, meta)

    print(predictedEarth['earthCoord'][5:10, 0:5])

    print(pixel[1, 0])




