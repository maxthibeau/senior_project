# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 08:38:29 2020

@author: The Skyentists
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
from RampFunctions import *

#The GPP class will hold variables and functions used in the GPP optimization process
class GPP:

  #Initializes the GPP class
  def __init__(self,pft,bplut,VPD_vals,SMRZ_vals,TMIN_vals,Par_vals,FPAR_vals): #,FT_mult
    # GPP: 5=LUEmax, 6=Tmin_min_K, 7=Tmin_max_K, 8=VPD_min_Pa, 9=VPD_max_Pa, 10=SMrz_min, 11=SMrz_max, 12=FT_min, 13=FT_max
    #from inputs
    self.Par_vals = Par_vals
    self.FPAR_vals = FPAR_vals
    self.VPD_vals = VPD_vals
    self.SMRZ_vals = SMRZ_vals
    self.TMIN_vals = TMIN_vals
    #from bplut
    self.lue = float(bplut[pft][5])
    self.VPD_min = float(bplut[pft][8]) #in Pa
    self.VPD_max = float(bplut[pft][9])
    self.SMRZ_min = float(bplut[pft][10])
    self.SMRZ_max = float(bplut[pft][11])
    self.TMIN_min = float(bplut[pft][6]) #in K
    self.TMIN_max = float(bplut[pft][7])
    self.FT_mult_min = float(bplut[pft][12])
    self.FT_mult_max = float(bplut[pft][13])
    #from calculations/for graph
    self.lue_vals = [0,self.lue]
    self.VPD_ramp = [] #x-axis for VPD ramp function
    for i in range(len(self.VPD_vals)):
        x_arr = self.VPD_vals[i]
        for y in range(len(x_arr)):
            x = x_arr[y]
            single_VPD = self.calc_ramp_VPD(x)
            self.VPD_ramp.append(single_VPD)
    self.TMIN_ramp = [] #x-axis for TMIN ramp function
    for q in range(len(self.TMIN_vals)):
        x_arr = self.TMIN_vals[q]
        for k in range(len(x_arr)):
            x = x_arr[k]
            single_TMIN = self.calc_ramp_TMIN(x)
            self.TMIN_ramp.append(single_TMIN)
    self.SMRZ_ramp = [] #x-axis for SMRZ ramp function
    for z in range(len(self.SMRZ_vals)):
        x_arr = self.SMRZ_vals[z]
        for p in range(len(x_arr)):
            x = x_arr[p]
            single_SMRZ = self.calc_ramp_SMRZ(x)
            self.SMRZ_ramp.append(single_SMRZ)
    self.gpp_vals = self.calc_gpp()
    self.y_vals = self.calc_y_ramp()
    self.display_ramps()

  #Calculates GPP (if not already given)
  def calc_gpp(self):
    APAR = self.calc_APAR(self.Par_vals,self.FPAR_vals)
    emults = self.calc_emult()
    gpp_vals = []
    for e in range(len(emults)):
        gpp = APAR * self.lue * emults[e] # self.lue is the same as Emax
        gpp_vals.append(gpp)
    return gpp_vals

  #Calculates APAR with inputs PAR and FPAR (APAR = PAR X FPAR)
  def calc_APAR(self, PAR, FPAR):
    pars = 0
    for p in range(len(PAR)):
        pars += PAR[p]
    par = pars / len(PAR)
    fpars = 0
    for f in range(len(FPAR)):
        fpars += FPAR[f]
    fpar = fpars / len(FPAR)
    apar = par * fpar
    return apar

  #Calculates E_mult (E_mult = f(VPD)*f(TMIN)*f(SMRZ)*FT_mult)
  def calc_emult(self):
    e_mults = []
    FT_mult = self.FT_mult_min
    if(len(self.VPD_ramp) != len(self.TMIN_ramp) and len(self.VPD_ramp) != len(self.SMRZ_ramp)):
        print("Error in length of VPD, TMIN, and SMRZ")
    else:
        for e in range(len(self.VPD_ramp)):
            E_mult = self.VPD_ramp[e] * self.TMIN_ramp[e] * self.SMRZ_ramp[e] * FT_mult
            e_mults.append(E_mult)
    return e_mults

  #Calculates the ramp function of SMRZ (f(SMRZ))
  def calc_ramp_SMRZ(self,x):
    val = 0
    if(x >= self.SMRZ_max):
        val = 1
    elif(x <= self.SMRZ_min):
        val = 0
    else:
        val = (x - self.SMRZ_min)/(self.SMRZ_max - self.SMRZ_min)
    return val

  #Calculates the ramp function of TMIN (f(TMIN))
  def calc_ramp_TMIN(self,x):
    val = 0
    if(x >= self.TMIN_max):
        val = 1
    elif(x <= self.TMIN_min):
        val = 0
    else:
        val = (x - self.TMIN_min)/(self.TMIN_max - self.TMIN_min)
    return val

  #Calculates the ramp function of VPD (f(VPD))
  def calc_ramp_VPD(self,x):
    val = 0
    if(x >= self.VPD_max):
        val = 1
    elif(x <= self.VPD_min):
        val = 0
    else:
        val = (x - self.VPD_min)/(self.VPD_max - self.VPD_min)
    return val

  def calc_y_ramp(self):
      emults = self.calc_emult()
      y_vals = []
      for e in range(len(emults)):
          y = self.lue * emults[e]
          y_vals.append(y)
      return y_vals

  #uses RampFunction class to display the ramp function graphs
  def display_ramps(self):
      vpd = RampFunction(self.VPD_ramp,self.y_vals,self.lue_vals,"VPD","GPP")
      vpd.display_ramp()
      tmin = RampFunction(self.TMIN_ramp,self.y_vals,self.lue_vals,"TMIN","GPP")
      tmin.display_ramp()
      smrz = RampFunction(self.SMRZ_ramp,self.y_vals,self.lue_vals,"SMRZ","GPP")
      smrz.display_ramp()

  def display_gpp_v_emult(self):
      pass

  #The GPP optimization function with no input (All outliers included)
  def optimize_gpp(self):
    pass

  #The GPP optimization function with given boolean list of what outliers to include
  #Input order: [LUE, VPD_min, VPD_max, SMRZ_min, SMRZ_max, TMIN_min, TMIN_max, FT_mult]
  def optimize_gpp(self,choice_vector):
    pass

  #Gets user input for what outliers to include and exclude for the use of the GPP optimization process
  #(For the use of the command line interface version of the program)
  def cli_get_input(self):
    choice = -1
    still_choosing = True
    #Default is all outliers included
    c_list = [True,True,True,True,True,True,True,True]

    print("Choose which parameters to include or exclude in optimization (all included by default):")
    print("0: Continue with optimization")
    print("1: LUE")
    print("2: VPD_min")
    print("3: VPD_max")
    print("4: SMRZ_min")
    print("5: SMRZ_max")
    print("6: TMIN_min")
    print("7: TMIN_max")
    print("8: FT_mult")
    print("9: View all parameter states (True = included, False = excluded)")

    while(still_choosing):

      try:
        choice = int(input("Which do you choose? (0-9): "))
      except ValueError:
        choice = -1

        if(choice == 0):

          still_choosing = False

        elif(choice > 0 & choice <= 8):

          c_list[choice-1] = not c_list[choice-1]

        elif(choice == 9):

          print("LUE:",c_list[0],"\nVPD_min:",c_list[1],"\nVPD_max:",c_list[2],"\nSMRZ_min:",c_list[3],"\nSMRZ_max:",c_list[4],"\nTMIN_min:",c_list[5],"\nTMIN_max",c_list[6],"\nFT_mult:",c_list[7])

        else:

          print("Invalid choice, please try again (0-9): ")


      return c_list
