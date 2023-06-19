from pandas import Series

class IonDataController():
    def get_seriesCPS(self, seriesIon:Series, samplerate:int)->Series:
        """returns seriesCPS based on seriesIon (IONDATA)

        Args:
            seriesIon (_pandas series_): series holding data/time for specfic ion
            samplerate (_int_): integer holding the the time it takes the massaspec to take a sample. for example: 46 microseconds

        Returns:
            __pandas series_: series holding the iondata corrected for samplerate
        """
        #initialise new series
        new_series = seriesIon.copy()
        try:
            seriesCPS = new_series*(1000000)/samplerate
            return seriesCPS
        except Exception as e:
            print(f"error in get_seriesCPS: {e}")
            return new_series
    
    def get_seriesCorrectedForBackground(self, seriesCPS:Series, BackGroundCorrectingSettings)->Series:
        """returns series of iondata (corrected for cps) corrected for background. 
        it lowers the values of seriesCPS by the average of the non-peak intervals

        Args:
            seriesCPS (_pandasseries_): series holding the iondata corrected for samplerate
            BackGroundCorrectingSettings (_class_): helperclass holding the integration bounds for the peaks
        """
            
        # set total_length and total_sum variables. average will be total_sum / total_length
        total_length = 0
        total_sum = 0

        #loop over all the intervals and calculate rolling sum and total length... 
        for interval in BackGroundCorrectingSettings.non_peak_intervals:
            #check for logical interval values
            try: 
                if interval[0]<interval[1]:
                    for index in range(interval[0], interval[1]):

                        total_sum += seriesCPS[index]

                        total_length +=1                            

            except: 
                raise ValueError("valueerror in getSeriesCorrectedForBackground ... most likely the values in non_peak_intervals are not integers ")
        #calculate the average. average will return 0 if no calculation could be made (len interval is 0 or incorrect values)
        try:
            average = total_sum / total_length
        except: 
            average = 0
        #initialise new series
        new_series = seriesCPS.copy()
        #detract the previously calculated average from every value in the new pandas series
        try:
            new_series -= average
        except: 
            raise ValueError("valueerror in getSeriesCorrectedForBackground ... could not detract background average from new pandas series ")
        
        return new_series
    

idc = IonDataController()  #singleton pattern
