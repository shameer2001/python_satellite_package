Tutorial - How to Use this Package
===================================

We will show you how to use this package with an example. The example involves obtaining query and download images for a particular date.


Once the package is installed, the query_isa function can be used to obtain the image data for a specific time frame and instrument. This is done by obtaining the data file itself. An example is shown below.

.. code-block:: 

    $ from aigeanpy.net import query_isa
    $ query_isa(start_date='2022-12-05', stop_date='2022-12-07', instrument = 'fand')




This will print all of the file information between these dates for the selected instrument. Then, you can select your desired file from the query result and download it using the filename:

.. code-block:: 

    $ from aigeanpy.net import download_isa
    $ download_isa('aigean_fan_20221206_182924.zip')




Finally, the images can be obtained using the get_satmap functtion methods:

.. code-block:: 
    
    $ from aigeanpy.satmap import get_satmap
    $ image = get_satmap('aigean_fan_20221206_182924.zip').visualise

You are also given the option to save the image (see the satmap.SatMap.visualise section in the documentation).