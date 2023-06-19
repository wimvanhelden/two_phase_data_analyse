import os
from..ExperimentData.ExperimentData_model import ExperimentData

class MemoryClassController():
    def get_list_file_adress_directory(self, location:str)->list:
        """returns a list with all file adresses of files in a directory

        Args:
            location (str): str of directory adress

        Returns:
            _list_: _list containing string of all file adresses in the direcotry_
        """   
        #future nice addition: make function recursive to crawl through subdirectories    
        list_file_adress = []
        for path in os.listdir(location):
            # check if current path is a file
            if os.path.isfile(os.path.join(location, path)):
                    list_file_adress.append(location+path)

        return list_file_adress



    def get_from_directory(self, location:str)->list:
        """handles loading experiment output TSV files into the memoryclass. 
        Returns a list with an ExperimentData object for each file in the location

        Args:
            location (str): str of directory adress

        Returns:
            _list_: a list with an ExperimentData object for each file in the location
        """
        try:
            list_files = self.get_list_file_adress_directory(location)
        except:
             list_files = []
        #initialise empty list of experimentdata:
        list_experimentdata = []
        #loop over the files and create experimentdata object if it loads
        for filename in list_files:
            try:
                ed = ExperimentData()
                ed.parse_from_file(filename)
                list_experimentdata.append(ed)
            except Exception as e:
                 print(f"error loading a TSV file in get_from_directory(): {e} for file: {filename}")                       
        return list_experimentdata

#initialise object (singleton)
mmc = MemoryClassController()

