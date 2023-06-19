import pandas as pd
from ..IonData.IonData_model import IonData



class TSV_Standard_Parser():
    """
    class that handles parsing a TSV (get data from contents, and from filename)
    """    
    _fileLocation = None  #string holding the filelocation of the CSV file
    _skiprows = 7  # integer value marking where which line the data starts in the file
    _list_names_non_ION_series = ["index", "time (ms)"]



    def get_dataframe(self, file_name_location:str)->pd.DataFrame:
        """returns a pandas dataframe holding all data from an experiment from a TSV file (output of the massaspec)

        Args:
            file_name_location (_str_): location of the massaspec output file (TSV file)

        Returns:
            _pandasdataframe_: pandas dataframe holding all data from an experiment from a TSV file
        """
        #possible addition: check if file_name_location exists. now its handled "ugly" with try...except...
        try:
            df = pd.read_table(file_name_location, skiprows=self._skiprows)
            return df
        except Exception as e:
            print("error in parsing TSV")
            print(e)
            return None

    def get_seriesTimeValues(self, dataframe:pd.DataFrame)->pd.Series:
        """returns the series holding the timevalues (ms values) from a dataframe 

        Args:
            returns the series holding the timevalues (ms values) from a dataframe 

        Returns:
            _pandasseries_: _pandasseries holding the time values of an experiment_
        """
        try:
            series = dataframe['time (ms)']
            return series
        except Exception as e:
            print("problem getting seriesTimeValues from dataframe")
            print(e)
            return None
        
    def get_listIonData(self, dataframe:pd.DataFrame)->pd.Series:
        """returns the series holding the timevalues (ms values) from a dataframe 

        Args:
            returns the series holding the timevalues (ms values) from a dataframe 

        Returns:
            _pandasseries_: _pandasseries holding the time values of an experiment_
        """
        try: 
            all_columnnames = dataframe.columns
            listIonData = []
            for columnname in all_columnnames:
                
                if columnname not in self._list_names_non_ION_series:
                    id = IonData()
                    id.seriesIon = dataframe[columnname]
                    id.name = columnname
                    listIonData.append(id)
                
            return listIonData
        except Exception as e:
            print("problem getting listIonData from dataframe")
            print(e)
            return None

          
    #function for getting a pandas data set from csv
    def read_data(filename:str, relative_location:str="./input", skiprows:int=7)->pd.DataFrame:
        """gets a pandas data set from tsv file

        Args:
            filename (str): name of file
            relative_location (str, optional): location of file. Defaults to "./input".
            skiprows (int, optional): number of rows to skip. Defaults to 7.

        Returns:
            _pandasdataframe_: dataframe holding experiment results
        """
        try: 
            build_file_location=relative_location + "/" + filename
            df = pd.read_table('../input/test1.txt', skiprows=7)
            return(df)
        except Exception as e:
            print(e)
            return None
    


