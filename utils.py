
import numpy as np
import json

def earth_to_pixel(earth_coord, meta):
    # todo: convert earth coordinates to pixels, provide the top-right corner of the earth coordinate
    ...


def pixel_to_earth(pixel_coord, meta):
    # convert pixels to earth coordinates, provide the coordinate of the centre of the pixel.

    resolution = float(meta['resolution'])
    xcoords = list(meta['xcoords'])
    ycoords = list(meta['ycoords'])

    fov = [int(xcoords[1] - xcoords[0]), int(ycoords[1] - ycoords[0])]

    columnCnt, rowCnt = [int(fov[0] / resolution), int(fov[1] / resolution)]
    xDist, yDist = [fov[0]/columnCnt, fov[1]/rowCnt]

    lowX, highX = xcoords
    lowY, highY = ycoords

    earth = [[0 for i in range(fov[0])] for j in range(fov[1])]

    if resolution >= 1:
        for i in range(len(earth)):
            for j in range(len(earth[0])):
                pixelX = int(j/xDist)
                pixelY = int(i/yDist)
                earth[i][j] = pixel_coord[pixelY][pixelX]
    else:
        pixelX, pixelY = 0, 0
        xStep, yStep = len(pixel_coord[0]) / fov[0], len(pixel_coord) / fov[1]
        # if 1 earth coord mapping multiple pixels, give the top-left corner
        for i in range(len(earth)):
            for j in range(len(earth[0])):
                earth[i][j] = pixel_coord[pixelY][pixelX]
                pixelX = int(pixelX + xStep)
            pixelY = int(pixelY + yStep)

    central = [[0 for i in range(len(pixel_coord[0]))] for j in range(len(pixel_coord))] if resolution >= 1 else None

    if resolution >= 1:
        # if 1 pixel mapping multiple earth coord, provide the coordinate of centre of the pixel
        for i in range(len(central)):
            for j in range(len(central[0])):
                central[i][j] = [lowX + xDist/2, lowY + yDist/2]
                lowX += xDist
                lowY += yDist

    return {'earthCoord': np.array(earth), 'centralCoord': None if central is None else np.array(central)}


if __name__ == "__main__":
    # the provided pixel array
    pixel = np.load('observation.npy')

    # the provided meta info
    f = open('metadata.json')
    meta = json.load(f)
    print(meta)

    map = pixel_to_earth(pixel, meta)
    print(map.get('centralCoord').shape)
    #predicted_pixel = earth_to_pixel(predicted_earth, meta)


    # assert np.alltrue(pixel == predicted_pixel)
