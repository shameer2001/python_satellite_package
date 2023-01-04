from ctypes import Union
from pathlib import Path


class SatMap:
    def __init__(self, meta, data, shape, fov, centre):
        self.meta = meta
        self.data = data
        self.shape = shape
        self.fov = fov
        self.centre = centre

    def mosaic(self, otherMap: 'SatMap', resolution: int, padding: bool) -> 'SatMap':
        # todo: allow to combine images as when using + but allowing mixing instruments (with different resolution!).
        ...

    def visualise(self, save: bool, savepath:Union(Path, str), **kwargs) -> None:
        # todo: Show the axis as in earth coordinates and with the proper orientation of the image.
        ...

    # todo: Also need to support the + and - operation
    def __add__(self, other):
        ...

    def __sub__(self, other):
        ...


def get_satmap(file_name) -> 'SatMap':
    # todo: Give the name of the file, and return the data and meta,
    #  where data gives the array, meta gives a dictionary with the metadata of the file.
    ...


