import sys
import matplotlib.pyplot as plt
import numpy as np

class RampFunction:
    def __init__(self,x_axis,y_axis,lue_vals,ramp,gpp_reco):
        self.figure = plt.figure()
        self._x_axis = x_axis #GPP: VPD,TMIN,SMRZ, RECO: SMSF,TSOIL
        self._y_axis = y_axis #GPP/APAR or Rh/Cbar
        self._lue = lue_vals
        self._title = ramp
        self._type = gpp_reco

    def display_ramp(self):
        print("X-AXIS",len(self._x_axis))
        print("Y-AXIS",len(self._y_axis))
        if(len(self._x_axis) != len(self._y_axis)):
            print("Error: invalid coordinates for ramp function",self._title)
            exit(1) #no further code in this function
        #ax = self.figure.add_subplot(111)
        #ax.clear()
        #ax.scatter(self._x_axis,self._y_axis)
        #ax.set_title("Ramp Function: " + self._title)
        #ax.set_xlabel(self._title)
        #ax.set_ylabel(self._type)
        #ax.show()
