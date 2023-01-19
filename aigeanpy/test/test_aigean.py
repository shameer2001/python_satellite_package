import pytest
from pathlib import Path
from aigeanpy.aigean_today import aigean_today
from aigeanpy.aigean_metadata import aigean_metadata
from aigeanpy.aigean_mosaic import aigean_mosaic
class Test_aigean_today(object):
    # the negative test
    def test_instrument_input_type_error(self):
        with pytest.raises(TypeError) as exception:
            aigean_today(self)
        assert str(exception.value) == "name of instrument inpute must be string"
    def test_instrument_input_value_error(self):
        with pytest.raises(ValueError) as exception:
            aigean_today(self)
        assert str(exception.value) == "names of instrument inpute is not available"
class Test_aigean_metadata(object):
    # the negative test
    def test_filename_input_type_error(self):
        with pytest.raises(TypeError) as exception:
            aigean_metadata(self)
        assert str(exception.value) == "name of files inpute must be string"
    def test_filename_input_value_error(self):
        with pytest.raises(ValueError) as exception:
            aigean_metadata(self)
        assert str(exception.value) == "name of files should in right format"
    # the positive test
    def test_function_return(self):
        # use 'aigean_man_20221205_194510.hdf5' as test sample
        output = aigean_metadata(self)
        assert output['archive:'] == 'ISA', "output is wrong"
        assert output['observatory:'] == 'Aigean', "output is wrong"
        assert output['instrument:'] == 'Manannan', "output is wrong"
        assert output['obs_date:'] == '2022-12-05 19:45:10', "output is wrong"
class Test_aigean_mosaic(object):
    # the negative test
    def test_input_value_error(self):
    # use 'aigean_man_20221205_194510.hdf5' as test sample
        with pytest.raises(ValueError) as exception:
            aigean_mosaic(self)
        assert str(exception.value) == "only two or more filename inputs are acceptable"


    
# the negative test
# test all these wrong inputs
test_1 = Test_aigean_today.test_instrument_input_type_error(123)
test_2 = Test_aigean_today.test_instrument_input_value_error('abc')
test_3 = Test_aigean_metadata.test_filename_input_type_error([123,251.23])
test_4 = Test_aigean_metadata.test_filename_input_value_error(['abc'])
test_5 = Test_aigean_mosaic.test_input_value_error(['aigean_man_20221205_194510.hdf5'])
# the positive test
# test with the sample file with it first 4 key elements.
test_6 = Test_aigean_metadata.test_function_return(['aigean_man_20221205_194510.hdf5'])
# it all passed