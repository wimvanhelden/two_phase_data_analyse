class FilenameParser():
    """class to parse properties from a stringname
    """
    #set index values for properties
    _index_timestamp = 0
    _index_gelatinName = 1
    _index_fluency = 3
    _index_laser_spot_diameter = 4
    _index_E_percent = 8    
    _string_filename = None
    _seperator_symbol_1 = "/"
    _seperator_symbol_2 = "."
    _seperator_symbol_3 = "_"
    _seperator_symbol_4 = "-"
    

    @property
    def filename(self)->str:
        if self._string_filename is not None:
            return self._string_filename
        else:
            raise AttributeError("filename is not set in FilenameParser")
    
    @filename.setter
    def filename(self, value:str):
        """sets filename and some other values used in later methods

        Args:
            value (_str_): string holding filelocation. for example: "C:/massaspec/output/15h33m42s_Gel1_Eseries_4mJ_20micron.h5__SegmentProfiles_Average.txt"

        Raises:
            ValueError: _function only excepts strings as input. raises error because values are critical_
        """
        if isinstance(value, str):
            self._string_filename = value
            try:
                self._list_string_filename_split = self.filename.split(self._seperator_symbol_1)
                #get the last element from that list
                self._string_filename = self._list_string_filename_split[len(self._list_string_filename_split)-1]
                self._list_filename_split = self._string_filename.split(self._seperator_symbol_3)
            except Exception as e:
                raise IndexError(f"problem setting filename: {e}")
        else:
            raise TypeError("filename in FilenameParser can only be set to a string value")
        
#set index values for each property (the location of those strings in list_filename_split)
    def give_timestamp(self)->str:
        """returns timestamp from filename

        Returns:
            _str_: string of experiment timestamp
        """
        try:
            return self._list_filename_split[self._index_timestamp]
        except Exception as e:
            print("problem parsing timestamp from filename:")
            print(e)
            return None
    

    def give_gelatinname(self)->str:
        """returns gelatinname from filename

        Returns:
            _str_: string of experiment gelatinname
        """
        try:
            return self._list_filename_split[self._index_gelatinName]
        except Exception as e:
            print("problem parsing gelatinname from filename:")
            print(e)
            return None
    

    def give_fluency(self)->str:
        """returns fluency from filename

        Returns:
            _str_: string of experiment fluency
        """
        try:
            return self._list_filename_split[self._index_fluency]
        except Exception as e:
            print("problem parsing fluency from filename:")
            print(e)
            return None
    
    
    def give_laser_spot_diameter(self)->str:
        """returns laser spot diameter from filename

        Returns:
            _str_: string of experiment laser spot diameter
        """
        try: 
            full_string = self._list_filename_split[self._index_laser_spot_diameter]
            list_split = full_string.split(self._seperator_symbol_2)
            return list_split[0]
        except Exception as e:
            print("problem parsing laser_spot_diameter from filename:")
            print(e)
            return None
        
    def give_E_percent(self)->str:
        """returns E_setting_% from filename

        Returns:
            _str_: string of experiment E_setting_%
        """       
        try:
            full_string = self._list_filename_split[self._index_E_percent]
            list_split = full_string.split(self._seperator_symbol_4)
            string_return = list_split[1].split(self._seperator_symbol_2)[0]
            return int(string_return)
        except Exception as e:
            print(f"problem parsing E_percent from filename: {self.filename}")
            print(e)
            return None

        





