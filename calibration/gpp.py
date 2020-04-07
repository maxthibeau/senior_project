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
from funcs.sse import *

#The GPP class will hold variables and functions used in the GPP optimization process
class GPP:

  #Initializes the GPP class
  def __init__(self, pft, bplut, meteor_input, flux_tower_data):
    # from flux tower data
    self._observed_gpp = flux_tower_data.gpp()
    self._non_missing_obs = flux_tower_data.non_missing_observations()
    self._tower_weights = flux_tower_data.weights()

    self._gpp_params = bplut.gpp_params(pft)
    # from meteor input
    self._VPD = meteor_input.VPD()
    self._TMIN = meteor_input.TMIN()
    self._SMRZ = meteor_input.SMRZ()
    self._FPAR = meteor_input.FPAR()
    # FPAR is 81 length array, observed gpp is a scalar, take mean to make dimensionality match
    self._FPAR = np.mean(self._FPAR, axis = 1)
    self._PAR = meteor_input.PAR()
    self._TSURF = meteor_input.TSURF()

    self._set_apar_bounds()

  def _set_apar_bounds(self):
    self._APAR = self._FPAR * self._PAR
    # prompt user for APAR bounds
    select_apar_bounds = None
    while (select_apar_bounds not in ("y", "n")):
      select_apar_bounds = input("would you like to specifiy APAR bounds?(y/n): ")
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
    simulated_gpp = gpp_apar(self._APAR, self._VPD, self._TMIN, self._SMRZ, self._TSURF, *gpp_params)
    return sse(self._observed_gpp, simulated_gpp, self._non_missing_obs, self._tower_weights)

  def simulated_gpp(self):
    # FIXME: make this simulated gpp
    return self._observed_gpp

  #uses RampFunction class to display the ramp function graphs
  def display_ramps(self):
    gpp_over_apar = self._observed_gpp / (self._APAR)
    lue, vpd_min, vpd_max, tmin_min, tmin_max, smrz_min, smrz_max, _, _ = self._gpp_params
    display_ramp(self._VPD, gpp_over_apar, downward_ramp_func, (vpd_min, vpd_max), lue, "VPD", "GPP/APAR")
    display_ramp(self._TMIN, gpp_over_apar, upward_ramp_func, (tmin_min, tmin_max), lue, "TMIN", "GPP/APAR")
    display_ramp(self._SMRZ, gpp_over_apar, upward_ramp_func, (smrz_min, smrz_max), lue, "SMRZ", "GPP/APAR")

  def display_gpp_v_emult(self):
    graph = RampFunction(self.e_mult,self.gpp,self.lue_vals,"Emult","GPP")
    print("Would you like to display the graph of GPP vs Emult?")
    choice = char(input("Y for Yes, N for No: "))
    if(choice.lower() == "y"):
      graph.display_optional()

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
