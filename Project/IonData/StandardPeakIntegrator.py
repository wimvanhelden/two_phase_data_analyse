class StandardPeakIntegrator():
    """class that handles the standard case for peak integration (two peak phenomenon)
    """

    interval_1 = [3,12] #list with the index values of the borders of first peak
    interval_2 = [13,50] #list with the index values of the borders of second peak

    def give_integrated_peaks(self, pandasseries)->int:
        """returns two values: integrated CPS peak signal for IonClass data

        Args:
            pandasseries (_series_): series holding CPS, corrected for background, signal (IONDATA)

        Raises:
            ValueError: most likely an index out of bounds

        Returns:
            _int_: total integrated signal of peak 1
            _int_: total integrated signal of peak 2
        """
        try:
            peak_1 = 0
            for index in range(self.interval_1[0],self.interval_1[1]):
                peak_1 += pandasseries[index]
            peak_2 = 0
            for index in range(self.interval_2[0],self.interval_2[1]):
                peak_2 += pandasseries[index]
            return peak_1, peak_2
        except:
            raise ValueError("problem integrating peaks with standard peak integrator. ")
        
#initialise object (singleton)     
spi = StandardPeakIntegrator()