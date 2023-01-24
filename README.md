# Finding water level changes via satellite imagery


## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
	- [Generator](#generator)
- [License](#license)

## Background

The Irish Space Agency has launched Aigean, an Earth observation satellite to monitor an area around 
Lough Ree. Recently, rainfall has decreased in the area, and during the latest years droughts have become
more frequent and more severe. With the instruments on board Aigean the scientific community will be
able to obtain better data about the water levels and the erosion of the land, and therefore will be able to
generate more accurate predictions. 
However, the Irish Space Agency sadly hasn’t provided any software tools to do this analysis!
Thankfully, Aoife O’Callaghan, a geology PhD student at the Athlone City Institute, has set the objective
to solve this problem by creating an open-source package to analyse Aigean data. Aoife has some ideas of
what she would like the package to do, but she doesn’t have a research software development background
beyond how to install and use Python libraries. That’s why Aoife has contacted you!
I and my group members agree this is a great tool to offer to the community and have decided to put all
your brains together to come up with an easy-to-use Python library to analyse and visualise Aigean satellite
data.

## Install

Please use the code below.

```sh
$ pip install .
```

## Usage

This is only a documentation package. You can print out [spec.md](spec.md) to your console:

```sh
$ standard-readme-spec
# Prints out the standard-readme spec

$ utils.pixel_to_earth()
# convert image to the earth coord from pixel coord

$ utils.earth_to_pixel()
# convert image to the pixel coord from earth coord

$ SatMap.__add__()
# self defined + operation, collate two images and create the new SatMap instance (i.e, if we got an image
# covering the (0,0)-(10,10) range and another from (12, 5)-(22,15), then we would end up with a “canvas”
# that goes from (0,0)-(22,15).)

$ SatMap.__sub__()
# self defined - operation, obtain a difference image to measure change between the days, which will only work
# when the data is overlapping. (i.e, if we have taken an image yesterday covering (0,0)-(10,10), and today
# another in the range of (5, 5)-(15, 15), the resultant image should be the difference between the both for
# the range (5, 5)-(10, 10).)

$ SatMap.mosaic()
# allow to combine images as when using + but allowing mixing instruments with different resolution

$ SatMap.visualise()
# visualise the image, show the axis as in earth coordinates and with the proper orientation of the image.
```

### Generator

To use the generator, look at [generator-standard-readme](https://github.com/RichardLitt/generator-standard-readme). There is a global executable to run the generator in that package, aliased as `standard-readme`.



### Contributors

This project exists thanks to all the people who contribute. 

[@QiangHu1](https://github.com/QiangHu1)
[@Ablert1213](https://github.com/Ablert1213)
[@EricZhang660](https://github.com/EricZhang660)
[@shameer2001](https://github.com/shameer2001)
[@Morphling2ooo](https://github.com/Morphling2ooo)

## License

[UCL](LICENSE) © 