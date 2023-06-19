import xlsxwriter
import math

class MemoryClassViewer():
    """class to handle outputs, views, ... for MemoryClass objects
    """
    
    minimal_CPS = 100000  #minimal, total (per gel, for every E_set_%) CPS count for an ion to be outputted to graph. Used to filter out non-used ions
    
    #setting a dictionary to translate E_set_% values to fluency values
    dict_Eset_fluency = {}
    dict_Eset_fluency[1]=0.07
    dict_Eset_fluency[2]=0.14
    dict_Eset_fluency[3]=0.21
    dict_Eset_fluency[4]=0.28
    dict_Eset_fluency[5]=0.35
    dict_Eset_fluency[6]=0.42
    dict_Eset_fluency[7]=0.49
    dict_Eset_fluency[8]=0.56
    dict_Eset_fluency[9]=0.63
    dict_Eset_fluency[10]=0.7
    dict_Eset_fluency[12]=0.84    
    dict_Eset_fluency[14]=0.98
    dict_Eset_fluency[16]=1.12
    dict_Eset_fluency[18]=1.26
    dict_Eset_fluency[20]=1.4
    dict_Eset_fluency[24]=1.68
    dict_Eset_fluency[28]=1.96
    dict_Eset_fluency[32]=2.24
    dict_Eset_fluency[36]=2.52
    dict_Eset_fluency[40]=2.8
    dict_Eset_fluency[45]=3.15
    dict_Eset_fluency[50]=3.5
    dict_Eset_fluency[55]=3.38
    dict_Eset_fluency[60]=4.2
    dict_Eset_fluency[65]=4.55
    dict_Eset_fluency[70]=4.9
    dict_Eset_fluency[75]=5.25
    dict_Eset_fluency[80]=5.6
    dict_Eset_fluency[85]=5.95
    dict_Eset_fluency[90]=6.3

   
    def create_excel(self, listIonNames:list, dictIonGelPeak:dict):
        """creates the excel for two-peak analysis. Excel is created in same directory as the .exe (or run.py file)

        Args:
            listIonNames (_list_): list of all ionnames in memoryclass
            dictIonGelPeak (_dict_): dictionary containing the sorted (routed) IonData's per fluency per gel
        """
        #initiate a new workbook:
        workbook = xlsxwriter.Workbook('Eseries_combined.xlsx')

        #add a format:
        bold = workbook.add_format({'bold': True})
        
        #loop over all the ionnames, create a worksheet for every ionname
        for ionname in listIonNames:
            #first check that enough signal was measured:
            try: 
                if dictIonGelPeak[ionname]["GelTotal"][dictIonGelPeak[ionname]["BestGel"]]>self.minimal_CPS:
                        

                    #worksheetnames dont allow certain special characters:
                    worksheetname = ionname.replace("[","").replace("]","")
                    #add the worksheet to the workbook
                    worksheet = workbook.add_worksheet(worksheetname)

                    #write, for example,: Element:  [53Cr]+
                    worksheet.write("A1", "Element:", bold)
                    worksheet.write("B1",ionname) 

                    #write gelatin + {gelatinname}, for example,: gelatin: gel2
                    worksheet.write("A2", "Gelatin:", bold)
                    worksheet.write("B2",dictIonGelPeak[ionname]["BestGel"]) 

                    #write column headers:
                    worksheet.write("A3","E%")
                    worksheet.write("B3","Fluence (J/cm²)")
                    worksheet.write("C3","log(Fluence)")
                    worksheet.write("D3","Total integrated signal (cps)")
                    worksheet.write("E3","P1 / Total (%)")
                    worksheet.write("F3","P2 / Total (%)")

                    #set column widths:
                    worksheet.set_column(1, 1, 19)
                    worksheet.set_column(2, 2, 10)
                    worksheet.set_column(3, 3, 23)
                    worksheet.set_column(4, 5, 11)


                    #printing all the experiment results in the excel:
                    row = 3
                    col = 0
                    dict_loop = dictIonGelPeak[ionname]["IonOfEset"]
                    
                    for eset in dict_loop:
                        iondata = dict_loop[eset]
                        worksheet.write(row, col, eset)
                        fluence = self.dict_Eset_fluency[eset]
                        worksheet.write(row, col+1, fluence)
                        
                        log_fluence =math.log(fluence) 

                        worksheet.write(row, col+2, log_fluence)
                        totalsignal = iondata.totalIntegratedSignal
                        
                        if totalsignal != 0:
                            P1 = int((iondata.integratedPeakSignal1 / totalsignal)*100)
                            P2 = int((iondata.integratedPeakSignal2 / totalsignal)*100)
                        else:
                            P1 = 0
                            P2 = 0
                        
                        worksheet.write(row, col+3, int(totalsignal))
                        worksheet.write(row, col+4, P1)
                        worksheet.write(row, col+5, P2)
                        row += 1
                        
                        #creating the first graph:

                        chart_peak = workbook.add_chart({'type': 'scatter'})

                        chart_peak.add_series({
                            'name':'P1/Total(%)',
                            'categories': "='" + worksheetname +"'!$B$4:$B$33",
                            'values':"='" + worksheetname +"'!$E$4:$E$33"  
                        })

                        
                        chart_peak.add_series({
                            'name':'P2/Total(%)',
                            'categories': "='" + worksheetname +"'!$B$4:$B$33",
                            'values':"='" + worksheetname +"'!$F$4:$F$33"  
                        })
                        
                        chart_peak.add_series({
                            'name':'total integrated signal',
                            'categories': "='" + worksheetname +"'!$B$4:$B$33",
                            'y2_axis' : True,
                            'values':"='" + worksheetname +"'!$D$4:$D$33", 
                            'trendline': {
                                'type': 'log',
                                'color' : 'green'                        
                            }
                        })
                        
                        
                        # settings for first graph:
                        
                        chart_peak.set_title({'name': ionname})
                        
                        chart_peak.set_x_axis({
                            'name': "Fluence (J/cm²)",
                            
                            
                        })
                        

                        chart_peak.set_y_axis({
                            'name': "Ratio (%)"
                        })


                        chart_peak.set_y2_axis({
                            'name': "Total integrated signal (CPS)"
                        })


                        chart_peak.set_size({'width': 800, 'height': 450})
                        
                        #insert first graph
                        worksheet.insert_chart('H5', chart_peak)
                        
                        # create second graph: 
                        chart_log = workbook.add_chart({'type': 'scatter'})

                        chart_log.add_series({
                            'name':'P1/Total(%)',
                            'categories': "='" + worksheetname +"'!$C$4:$C$33",
                            'values':"='" + worksheetname +"'!$E$4:$E$33"  
                        })

                        
                        chart_log.add_series({
                            'name':'P2/Total(%)',
                            'categories': "='" + worksheetname +"'!$C$4:$C$33",
                            'values':"='" + worksheetname +"'!$F$4:$F$33"  
                        })

                        # settings for second graph:
                        chart_log.set_title({'name': ionname})

                        chart_log.set_x_axis({
                            'name': "log(Fluence)"
                        })


                        chart_log.set_y_axis({
                            'name': "Ratio (%)"
                        })


                        chart_log.set_size({'width': 800, 'height': 450})
                        
                        
                        #insert second graph
                        worksheet.insert_chart('H30', chart_log)
            except Exception as e:
                print(f"error in creating excel: {e}")   
                     

        #create the workbook with close() method    
        try:    
            workbook.close()
        except Exception as e:
            print("error in saving the workbook using .close() function: {e}")


#initialise object (singleton) 
mcv = MemoryClassViewer()