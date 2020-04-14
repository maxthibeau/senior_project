# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 08:38:29 2020

@author: The Skyentists
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import math
from RampFunctions import *
from funcs.gpp_funcs import *
from funcs.ramp_func import *
from funcs.sse import *

#The GPP class will hold variables and functions used in the GPP optimization process
class GPP:

  #Initializes the GPP class
  def __init__(self, pft, bplut, meteor_input, flux_tower_data):
    # from flux tower data
    self._observed_gpp = flux_tower_data.gpp()
    self._observed_gpp = self.clean_nans(self._observed_gpp)
    self._non_missing_obs = flux_tower_data.non_missing_observations()
    self._tower_weights = flux_tower_data.weights()

    self._gpp_params = bplut.gpp_params(pft)
    # from meteor input
    self._VPD = meteor_input.VPD()
    self._VPD = self.clean_nans(self._VPD)
    self._TMIN = meteor_input.TMIN()
    self._TMIN = self.clean_nans(self._TMIN)
    self._SMRZ = meteor_input.SMRZ()
    self._SMRZ = self.clean_nans(self._SMRZ)
    self._FPAR = meteor_input.FPAR()
    # FPAR is 81 length array, observed gpp is a scalar, take mean to make dimensionality match
    self._FPAR = np.mean(self._FPAR, axis = 1)
    self._PAR = meteor_input.PAR()
    self._TSURF = meteor_input.TSURF()
    self._TSURF = self.clean_nans(self._TSURF)

    self._set_apar_bounds()

    self._simulated_gpp = gpp_apar(self._APAR, self._VPD, self._TMIN, self._SMRZ, self._TSURF, *bplut.gpp_params(pft))

  def _set_apar_bounds(self):
    self._APAR = self._FPAR * self._PAR
    # prompt user for APAR bounds
    select_apar_bounds = None
    while (select_apar_bounds not in ("y", "n")):
      select_apar_bounds = input("Would you like to specifiy APAR bounds? (y/n): ")
    if select_apar_bounds == "y":
      self._apar_low_bound = float(input("Input a lower bound for apar (float): "))
      self._apar_high_bound = float(input("Input a higher bound for apar (float): "))
    elif select_apar_bounds == "n":
      self._apar_low_bound = np.min(self._APAR)
      self._apar_high_bound = np.max(self._APAR)
    # throw out all apar values that don't fall within bounds
    invalid_apar_indices = (self._APAR < self._apar_low_bound) & (self._APAR > self._apar_high_bound)
    self._APAR[invalid_apar_indices] = np.nan

  #Input order: [LUE, VPD_min, VPD_max, SMRZ_min, SMRZ_max, TMIN_min, TMIN_max, FT_mult]
  # NOTE: simulated GPP values are much lower than observed GPP values
  def func_to_optimize(self, gpp_params):
    self._simulated_gpp = gpp_apar(self._APAR, self._VPD, self._TMIN, self._SMRZ, self._TSURF, *gpp_params)
    return sse(self._observed_gpp, self._simulated_gpp, self._non_missing_obs, self._tower_weights)

  def simulated_gpp(self):
    return self._simulated_gpp

  #uses RampFunction class to display the ramp function graphs
  def display_ramps(self):
    gpp_over_apar = self._observed_gpp / (self._APAR)
    lue, vpd_min, vpd_max, tmin_min, tmin_max, smrz_min, smrz_max, _, _ = self._gpp_params
    choose = True
    while choose:
        try:
          char = input("Would you like to view GPP Ramp Functions with the current BPLUT values? (y/n): ")
        except ValueError:
          char = -1
        if(char=='n'):
          choose = False
        elif(char=='y'):
          display_ramp(self._VPD, gpp_over_apar, downward_ramp_func, (vpd_min, vpd_max), lue, "VPD", "GPP/APAR")
          display_ramp(self._TMIN, gpp_over_apar, upward_ramp_func, (tmin_min, tmin_max), lue, "TMIN", "GPP/APAR")
          display_ramp(self._SMRZ, gpp_over_apar, upward_ramp_func, (smrz_min, smrz_max), lue, "SMRZ", "GPP/APAR")
          choose = False
        else:
          print("Invalid value: please try again")

  def gpp_v_emult(self,pft,bplut,gpp_params):
    emults = emult(self._VPD, self._TMIN, self._SMRZ,  self._TSURF, *gpp_params)
    print("EMULTS: ",emults)
    graph = RampFunction(emults,self._observed_gpp,bplut[pft,"LUEmax"],"Emult","GPP")
    choose = True
    while choose:
        try:
           choice = input("Would you like to display the optional graph of GPP vs Emult? (y/n): ")
        except ValueError:
          choice = -1
        if(choice == 'n'):
          choose = False
        elif(choice == 'y'):
          graph.display_optional()
          choose = False
        else:
          print("Invalid value: please try again")

  def display_optimized_ramps(self,pft,new_bplut):
    print("OBSERVED GPP: ",self._observed_gpp)
    print("SIMMED GPP: ",self._simulated_gpp)
    gpp_params = new_bplut.gpp_params(pft)
    #can get RuntimeWarning here
    sim_gpp_over_apar = self._simulated_gpp / (self._APAR)
    lue, vpd_min, vpd_max, tmin_min, tmin_max, smrz_min, smrz_max, _, _ = gpp_params
    display_ramp(self._VPD, sim_gpp_over_apar, downward_ramp_func, (vpd_min, vpd_max), lue, "VPD", "GPP/APAR")
    display_ramp(self._TMIN, sim_gpp_over_apar, upward_ramp_func, (tmin_min, tmin_max), lue, "TMIN", "GPP/APAR")
    display_ramp(self._SMRZ, sim_gpp_over_apar, upward_ramp_func, (smrz_min, smrz_max), lue, "SMRZ", "GPP/APAR")

  def clean_nans(self,array): #array input
    for i in range(len(array)): #getting rid of nans in observed GPP
        arr = array[i]
        for x in range(len(arr)):
          if math.isnan(arr[x]) or arr[x]<0:
              arr[x] = 0
    return array

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
