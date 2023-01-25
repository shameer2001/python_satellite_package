from aigeanpy.net import *
import unittest
from unittest.mock import patch


class TestQueryIsa(unittest.TestCase):
    @patch('requests.get')
    def test_query_isa_no_connection(self, mock_get):

        # Configure the mock to raise a connection error
        mock_get.side_effect = requests.exceptions.ConnectionError # "simulate" connection error

    
      
        try:
            query_isa("2022-12-05", "2022-12-05", "lir")
        except ConnectionError as e:
            assert str(e) == "There is no (or a very weak) internet connection."

        else:
            assert False, "ConnectionError not raised for no internet connection for the query_isa() function."
        
    @patch('requests.get')
    def test_query_isa_no_connection_2(self, mock_get):

        mock_get.side_effect = requests.exceptions.ConnectionError 


        try:
            query_isa("2022-12-06", "2022-12-07", "lir")
        except ConnectionError as e:
            assert str(e) == "There is no (or a very weak) internet connection."

        else:
            assert False, "ConnectionError not raised for no internet connection for the query_isa() function."





class TestDownloadIsa(unittest.TestCase):
    @patch('requests.get')
    def test_download_isa_no_connection(self, mock_get):

        mock_get.side_effect = requests.exceptions.ConnectionError 

    
      
        try:
            download_isa("aigean_lir_20221215_094830.asdf")
        except ConnectionError as e:
            assert str(e) == "There is no (or a very weak) internet connection."

        else:
            assert False, "ConnectionError not raised for no internet connection for the download_isa() function."
        
    @patch('requests.get')
    def test_download_isa_no_connection_2(self, mock_get):

        mock_get.side_effect = requests.exceptions.ConnectionError 


        try:
            download_isa("'aigean_fan_20221217_075458.zip'")
        except ConnectionError as e:
            assert str(e) == "There is no (or a very weak) internet connection."

        else:
            assert False, "ConnectionError not raised for no internet connection for the download_isa() function."







if __name__ == '__main__':
    unittest.main()
