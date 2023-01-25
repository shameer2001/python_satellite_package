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

This is only a documentation package.
```sh
$ aigean_today [--instrument <instrument>] [--saveplot]
# Getting the latest image of the archive. It also accept a instrument argument and a saveplot argument.

$ aigean_metadata <filename_i>[<filename_j> ...]
# Extracting the metadata information from one file or a list of them

$ aigean_mosaic [--resolution <resolution>] <filename_i><filename_j>[<filename_k> ...]
# Creating a mosaic from the command line. It accept a resolution argument and two or more filenames.

$ python clustering_numpy.py <csv_file.csv> --iters <iters>
# Use kmean algorithm (numpy version) to classify dataset provided.

$ python
>>> from aigeanpy.net import query_isa
>>> lir_map = query_isa(start_date, stop_date, instrument)
# Accepts the same parameters as the webservice and returns a data structure with the details of the response.

$ python
>>> from aigeanpy.net import download_isa
>>> lir_map = download_isa(filename, save_dir)
# Accepts a filename obtained from querying the archive and downloads the file under the path.

$ python
>>> from aigeanpy.satmap import get_satmap
>>> lir_map = get_satmap(filename)
# Accepts a filename obtained from querying the archive and returns Satmap object.
```

### Contributors

This project exists thanks to all the people who contribute. 

[@QiangHu1](https://github.com/QiangHu1)
[@Ablert1213](https://github.com/Ablert1213)
[@EricZhang660](https://github.com/EricZhang660)
[@shameer2001](https://github.com/shameer2001)
[@Morphling2ooo](https://github.com/Morphling2ooo)

## License

[UCL](LICENSE) © 