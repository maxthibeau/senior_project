# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 08:38:29 2020

@author: The Skyentists
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
from RampFunctions import *
from funcs.gpp_funcs import *
from funcs.ramp_func import *

#The GPP class will hold variables and functions used in the GPP optimization process
class GPP:

  #Initializes the GPP class
  def __init__(self,pft,bplut,vpd,smrz,tmin,par,fpar): #,FT_mult
    lue = float(bplut[pft, 'LUEmax'])
    # a tuple here is (min, max)
    vpd_min = float(bplut[pft, 'VPD_min_Pa']) #in Pa
    vpd_max = float(bplut[pft, 'VPD_max_Pa'])
    tmin_min = float(bplut[pft, 'Tmin_min_K']) #in K
    tmin_max = float(bplut[pft, 'Tmin_max_K'])
    smrz_min = float(bplut[pft, 'SMrz_min'])
    smrz_max = float(bplut[pft, 'SMrz_max'])
    ft_mult_min = float(bplut[pft, 'FT_min'])
    ft_mult_max = float(bplut[pft, 'FT_max'])
    #from calculations/for graph
    self.lue_vals = [0,lue]
    e_mult = calc_e_mult(vpd, (vpd_min, vpd_max), tmin, (tmin_min, tmin_max), smrz, (smrz_min, smrz_max), 0)
    gpp = calc_gpp(fpar, par, epsilon_max, e_mult)
    # APAR = fpar * par
    y_vals = gpp / (fpar * par)
    print(y_vals)
    # self.display_ramps()

  #Calculates the ramp function of SMRZ (f(SMRZ))
  def calc_ramp_SMRZ(self,x):
    return ramp_func(x, self.SMRZ_min, self.SMRZ_max)

  #Calculates the ramp function of TMIN (f(TMIN))
  def calc_ramp_TMIN(self,x):
    return ramp_func(x, self.TMIN_min, self.TMIN_max)

  #Calculates the ramp function of VPD (f(VPD))
  def calc_ramp_VPD(self,x):
    return ramp_func(x, self.VPD_min, self.VPD_max)

  # this is gpp
  def calc_y_ramp(self):
      emults = self.calc_emult()
      y_vals = []
      for e in range(len(emults)):
          y = self.lue * emults[e]
          y_vals.append(y)
      return y_vals

  #uses RampFunction class to display the ramp function graphs
  def display_ramps(self):
      vpd = RampFunction(self.ramp_VPD,self.y_vals,self.lue_vals,"VPD","GPP")
      vpd.display_ramp()
      #tmin = RampFunction(self.TMIN_ramp,self.y_vals,self.lue_vals,"TMIN")
      #tmin.display_ramp()
      #smrz = RampFunction(self.SMRZ_ramp,self.y_vals,self.lue_vals,"SMRZ")
      #smrz.display_ramp()

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
