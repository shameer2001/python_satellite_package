import pytest
from pathlib import Path
from aigean_today import aigean_today
from aigean_metadata import aigean_metadata
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

    
# the negative test
test_1 = Test_aigean_today.test_instrument_input_type_error(123)
test_2 = Test_aigean_today.test_instrument_input_value_error('abc')
test_3 = Test_aigean_metadata.test_filename_input_type_error([123,251.23])
test_4 = Test_aigean_metadata.test_filename_input_value_error(['abc'])
# the positive test
test_5 = Test_aigean_metadata.test_function_return(['aigean_man_20221205_194510.hdf5'])
# it all passed