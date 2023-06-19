from .MemoryClass_controller import mmc
from .MemoryClass_viewer import mcv

class MemoryClass():
    """main class of the program. Holds all data loaded from massaspec. Holds all processing data. 

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    _listExperimentData = []  #central list of this class. Hold all the data in memory
    _listIonNames = []  #list of all IonNames. produced from listExperimentData. 
    _listGelatinNames = [] #list of all GelatinNames. produced from listExperimentData. 
    _listEset = [] ##list of all E_Set_% values. produced from listExperimentData. 
    
    _dictIonGelPeak = {} #dictionary used to select, for each Ion, the gel with most result. See documentation. 
    viewer = mcv  #set the viewer to instance of standard mcv
    controller = mmc  #set controller to default 

    @property
    def listExperimentData(self)->list:
        return self._listExperimentData
    
    @listExperimentData.setter
    def listExperimentData(self, value:list):
        self._listExperimentData = value

    @property
    def listIonNames(self)->list:
        return self._listIonNames
    
    @listIonNames.setter
    def listIonNames(self, value:list):
        self._listIonNames = value

    @property
    def listGelatinNames(self)->list:
        return self._listGelatinNames
    
    @listGelatinNames.setter
    def listGelatinNames(self, value:list):
        self._listGelatinNames = value

    @property
    def dictIonGelPeak(self)->dict:
        return self._dictIonGelPeak
    
    @dictIonGelPeak.setter
    def dictIonGelPeak(self, value:dict):
        self._dictIonGelPeak = value

    @property
    def listEset(self)->list:
        return self._listEset
    
    @listEset.setter
    def listEset(self, value:list):
        self._listEset = value



    def load_from_directory(self, location:str):
        """call the controller to load all massaspec files in a location (directory adress) into memory

        Args:
            location (_str_): _string of directory adress holding the massaspec output files_
        """
        self.listExperimentData = self.controller.get_from_directory(location)


    def set_all_seriesCPS(self):
        """sets all CPSseries in all iondatas in all experimentdatas 
        """
        for experimentdata in self.listExperimentData:
            experimentdata.set_all_seriesCPS()

    def set_all_seriesCorrectedBackground(self):
        """sets all CorrectedBackgroundseries in all iondatas in all experimentdatas 
        """
        for experimentdata in self.listExperimentData:
            experimentdata.set_all_seriesCorrectedBackground()

    def set_all_peak_signals(self):
        """sets all Peak Signals and total signals in all iondatas in all experimentdatas 
        """
        for experimentdata in self.listExperimentData:
            experimentdata.set_all_peak_signals()

    def set_ionnames_gels_peakdata_Eset(self):
        """creates:
         -  self.listIonNames: list of all ionnames in memoryclass
         - self.listGelatinNames: list of all gelnames in memoryclass
         - self.listEset: list of all Eset values in memoryclass
        """
        #check that all the preparation calculations are set, if not: do them
        self.set_all_seriesCPS()
        self.set_all_seriesCorrectedBackground()
        self.set_all_peak_signals()

        #loop over all experimentdata's 
        #put all IonNames (f.e. "[23Na]+ mmass 14.0025)" in list_IonNames
        #put all Gelnames (f.e. "gel1" in list_gelNames)
        #check if peak values are calculated, if not: calculate
        for Experimentdata in self.listExperimentData:
            if Experimentdata.gelatinName not in self.listGelatinNames:
                self.listGelatinNames.append(Experimentdata.gelatinName)
            if Experimentdata.E_setpoint_procent not in self.listEset:
                self.listEset.append(Experimentdata.E_setpoint_procent)
            for Iondata in Experimentdata.listIonData:
                if Iondata.name not in self.listIonNames:
                    self.listIonNames.append(Iondata.name)
                if Iondata.totalIntegratedSignal is None:
                    Iondata.set_peak_signals()
        #sort the list of gelatinnames alpahbetically:            
        self.listGelatinNames.sort()
        self.listEset.sort()


    def initialise_dictIonGelPeak(self):
        """sets dictIonGelPeak, used to select and store the best gel for each ion. Nested dictionary. See documentation. 
        """
        #clear dictIonGelpeak (has to start from empty):
        self.dictIonGelPeak = {}
        #check if ionnames and gelnames are set
        if len(self.listGelatinNames) == 0 or len(self.listIonNames) == 0:
            raise Exception("error initialising dictIonGelPeak in memoryclass")
        #create a dictionary per Ionname. Key = Ionname, value = dictionary
        for IonName in self.listIonNames:
            self.dictIonGelPeak[IonName] = {}
            #in the "ionname" value (dict) create a subdictionary with key "GelTotal"
            self.dictIonGelPeak[IonName]["GelTotal"]={}
            for gelname in self.listGelatinNames:
                # in the "geltotal" value populate with a dictionary with gelnames as key and 0 as value
                # that 0 will be used as a rolling sum value later in the summation
                self.dictIonGelPeak[IonName]["GelTotal"][gelname] = 0

    def calculate_gel_per_ionname(self):
        """sets a dictionary value holding the gelname with the most total signal captured for each ion. 
        """
        for experimentdata in self.listExperimentData:
            for iondata in experimentdata.listIonData:
                self.dictIonGelPeak[iondata.name]["GelTotal"][experimentdata.gelatinName] += iondata.totalIntegratedSignal

        for ionname in self.dictIonGelPeak:
            self.dictIonGelPeak[ionname]["BestGel"] = max(self.dictIonGelPeak[ionname]["GelTotal"], key=self.dictIonGelPeak[ionname]["GelTotal"].get)

        
    def set_IonOfEset_dict(self):
        """sets a dictionary that holds all IonData objects, of the gel selected, per E_set_% value
        """
        #loop over all ionnames to create the first layer of keys in the dictionary
        for ionname in self.listIonNames:
            self.dictIonGelPeak[ionname]["IonOfEset"] = {}
            gelchosen = self.dictIonGelPeak[ionname]["BestGel"]
            #loop over the E_set_% values to create the second layer of keys in the dictionary
            for Eset in self.listEset:
                #loop over the iondatas in experimentdatas to find match for E_set_% and gel_chosen
                for experimentdata in self.listExperimentData:
                    if experimentdata.gelatinName == gelchosen and experimentdata.E_setpoint_procent == Eset:
                        for iondata in experimentdata.listIonData:
                            if iondata.name == ionname:
                                self.dictIonGelPeak[ionname]["IonOfEset"][Eset] = iondata
                                #break here to save a bunch of time
                                break

    def make_excel(self):
        """calls viewer object to create an excel file in same directory as main file. calls the previous calculations. 
        Assumes that set_ionnames_gels_peakdata_Eset(self) ran previous to this function. 
        """
        self.initialise_dictIonGelPeak()
        self.calculate_gel_per_ionname()
        self.set_IonOfEset_dict()
        mcv.create_excel(self.listIonNames, self.dictIonGelPeak)

       

#initialise object (singleton)    
mc = MemoryClass()







    