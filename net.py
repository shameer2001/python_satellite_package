from requests import *
from pathlib import Path
from datetime import datetime as dt
from datetime import timedelta

class net:
    todays_date = dt.today().strftime('%Y-%m-%d')

    def query_isa(start_date = todays_date, stop_date = todays_date, instrument = None):
        """Returns a JSON file of the results from the query service. 
        
        Parameters
        ----------
        start_date : str (date of format YYYY-mm-dd), optional
                     Look for data in query catalogue taken on this date and further. Default is the current date.

        stop_date : str (date of format YYYY-mm-dd), optional
                    Look for data in query catalogue taken on this date and sooner. Default is the current date.
    
    
        instrument : str, optional
                     One of the possible image-taking instruments: 'lir', 'manannan', 'fand' or 'csvfile'. The function only includes data taken with the select instrument. Default is None (ie. the function searches for all).
                     
                     
        Notes
        -----
        A date is assigned to each data which represenets when the data was taken.
        Queries larger than 3 days are not allowed.

    
    
    
        Returns
        -------
        file: list
              Contains the data (each instant in a dictionary) extracted from the ISA archive. The file includes properties of the observations found in the specified time range and instruments (ie. the inputs)

    
    
        """
        # Error messages for incorrect inputs:
         
        if type(start_date) != str:
            raise TypeError("The start date must be a string in the form YYYY-mm-dd.")
            
        if type(stop_date) != str:
            raise TypeError("The stop date must be a string in the form YYYY-mm-dd.")
            
        if type(instrument) != str and (instrument != None):
            raise TypeError("The instrument name must be string.")
            

        # this will print a ValueError if dates are not in the correct format of YYYY-mm-dd (error messages built into datetime library)
        start_date_dt = dt.strptime(start_date, "%Y-%m-%d") 
        stop_date_dt = dt.strptime(stop_date, "%Y-%m-%d")
           
        if start_date_dt > stop_date_dt:
            raise ValueError("The start date must be earlier than the stop date.")
            
        if stop_date_dt - start_date_dt > timedelta(3): # error for queries larger than three days
            raise ValueError("Queries larger than three days are not allowed.") 



        # Obtain data:
        
        payload = {'start_date':start_date, 'stop_date':stop_date, 'instrument': instrument}
        r=get('https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/query/', params=payload)



        # Print errors from json file:
        for i in r.json():
            if i=='message':
                error_message = r.json()['message']
                print(error_message)
            else:
                return r.json() # Return json file
        


        
    def download_isa(filename, save_dir = None) -> None:
        """Downloads the data from the search done by the `net.query_isa()` function.


        Parameters
        ----------
        filename : str
                   Name of a file as provided by the `net.query_isa()` function.
    

    
    
        save_dir : str or path object, optional
                   The directory to save the file in. Default is None (ie download to current working directory)
                


        Notes
        -----

    
    
        """

        # Error messages for incorrect inputs:
        if type(filename) != str:
            raise TypeError("The filename must be a string.")
                       
        if type(save_dir) != str and save_dir != None:
          raise TypeError("The `save_dir` variable is not a string.")



        if save_dir:
            p = Path('{}/{}'.format(save_dir, filename))
            
            
            if not Path(save_dir).exists(): # if no such path exists
                raise NotADirectoryError("The directory given, for the `save_dir` variable, does not exist.")
                
        else:
            p = Path(filename) # with full name to save with correct extension



        # Obtain request from server:
        payload = {'filename':filename}
        r = get('https://dokku-app.dokku.arc.ucl.ac.uk/isa-archive/download/', params=payload)

        p.write_bytes(r.content) #download



print(net.query_isa("2022-12-05", "2022-12-06", "lir") )
#print(type(query_isa("2022-12-05", "2022-12-06", "lir") ))

net.download_isa("aigean_lir_20221205_191610.asdf")