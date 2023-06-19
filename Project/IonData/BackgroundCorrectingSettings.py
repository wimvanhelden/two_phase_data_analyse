class BackGroundCorrectingSettings():
    """helper class holding values used for correcting the background "noise" on IonData series
    """
    bool_calculate_automaticly = False  #set to true to calculate the non-peak intervals automaticly
    non_peak_intervals = [[0,2],[54,66]]