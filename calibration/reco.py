# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 22:44:33 2020

@author: The Skyentists
"""

import sys
import matplotlib.pyplot as pltkm
import numpy as np
import math
from AnalyticalModelSpinUp import *
from NumericalModelSpinUp import *
#from PreliminarySpinUp import *
from RampFunctions import *
from funcs.ramp_func import *
from funcs.reco_funcs import *
from funcs.sse import *

#The RECO class will hold variables and functions used in the RECO optimization process
class RECO:

  #Initializes the RECO class
  def __init__(self, pft, bplut, gpp, meteor_input, flux_tower_data):
    # RECO: 14=SMtop_min, 15=SMtop_max, 16=Tsoil_beta0, 17=Tsoil_beta1, 18=Tsoil_beta2, 19=fraut, 20=fmet, 21=fstr, 22=kopt, 23=kstr, 24=kslw

    self._prh = 0
    self._pk = 0
    self._set_prh_and_pk()

    self._gpp = gpp
    self._non_missing_obs = flux_tower_data.non_missing_observations()
    self._tower_weights = flux_tower_data.weights()
    # Rh = NEE
    self._observed_r_h = flux_tower_data.nee()
    self._observed_reco = flux_tower_data.reco()

    self._TSOIL = meteor_input.TSOIL()
    self._SMSF = meteor_input.SMSF()

    self._reco_params = bplut.reco_params(pft)
    self._lue = float(bplut[pft, 'LUEmax'])

    self._kmult = None
    self._cbar = None
    # run reco simulation once to get data for ramp funcs
    self.reco = self._simulate_reco(self._reco_params)

    # TODO: this might be the right way to calculate cbar
    # self._kmult_1km, self._npp_1km, _ = preliminary_spinup(pft, bplut, meteor_input)
    # _, _, _, self._c_bar = analytical_model_spinup(pft, bplut, self._kmult_1km, self._npp_1km)


  #Sets prh and pk
  def _set_prh_and_pk(self):
    still_choosing = True
    while(still_choosing):
      try:
        self._prh = float(input("Please specify a Prh (decimal between 0 and 1): "))
        self._pk = float(input("Please specify a Pk (decimal between 0 and 1): "))
      except ValueError:
        self._prh = -1
        self._pk = -1
      if(self._pk <= 1.0 and self._pk >= 0.0 and self._prh <= 1.0 and self._prh >= 0.0):
        still_choosing = False
      else:
        print("Invalid value: please try again")

  #uses RampFunction class to display the ramp function graphs
  def display_ramps(self):
    #rh_over_cbar = abs(self._observed_r_h / self._cbar) #did absolute to get rid of negatives
    rh_over_cbar = self._observed_r_h / self._cbar
    for i in range(len(rh_over_cbar)):
        for val in rh_over_cbar[i]:
            if(val<0):
                rh_over_cbar[i] = 0
    fraut, bt_soil, SMSF_min, SMSF_max = self._reco_params
    choose = True
    while choose:
        try:
          char = input("Would you like to view RECO Ramp Functions with the current BPLUT values? (y/n): ")
        except ValueError:
          char = -1
        if(char=='n'):
          choose = False
        elif(char=='y'):
          display_ramp(self._TSOIL, rh_over_cbar, kmult_arrhenius_curve, (bt_soil,), self._lue, "TSOIL", "Rh/Cbar")
          display_ramp(self._SMSF, rh_over_cbar, upward_ramp_func, (SMSF_min, SMSF_max), self._lue, "SMSF", "Rh/Cbar")
          choose = False
        else:
          print("Invalid value: please try again")

  def _simulate_reco(self, reco_params):
    fraut, bt_soil, smsf_min, smsf_max = reco_params
    self._kmult = kmult(self._TSOIL, self._SMSF, bt_soil, smsf_min, smsf_max)
    # prh/pk filtering
    min_kmult = np.percentile(self._kmult, self._pk)
    self._kmult[self._kmult < min_kmult] = np.nan
    #can get divide by zero encountered RuntimeWarning here
    rh_over_kmult = self._observed_r_h / self._kmult
    self._cbar = np.nanpercentile(self._kmult, self._prh, axis = 0)
    return reco(self._gpp, self._kmult, self._cbar, fraut)

  def func_to_optimize(self, reco_params):
    simulated_reco = self._simulate_reco(reco_params)
    return sse(self._observed_reco, simulated_reco, self._non_missing_obs, self._tower_weights)

  def rhc_v_kmult(self):
    rh_over_cbar = self._observed_r_h / self._cbar
    graph = RampFunction(self.get_kmult(),rh_over_cbar,self.lue_vals,"Kmult","GPP")
    choose = True
    while choose:
        try:
           choice = input("Would you like to display the optional graph of Rh/Cbar vs Kmult? (y/n):")
        except ValueError:
           choice = -1
        if(choice=='n'):
           choose = False
        elif(choice=='y'):
           graph.display_optional()
           choose = False
        else:
           print("Invalid value: please try again")

  def get_kmult(self):
      return self._kmult

  def get_reco(self):
      return self.reco

  def display_optimized_ramps(self,pft,new_bplut):
    reco_params = new_bplut.reco_params(pft)
    #rh_over_cbar = abs(self._observed_r_h / self._cbar) #did absolute to get rid of negatives
    new_reco = self._simulate_reco(reco_params)
    rh_over_cbar = self._observed_r_h / self._cbar
    for i in range(len(rh_over_cbar)):
        arr = rh_over_cbar[i]
        for val in range(len(arr)):
            if(arr[val]<0):
                arr[val] = 0
    fraut, bt_soil, SMSF_min, SMSF_max = reco_params
    display_ramp(self._TSOIL, rh_over_cbar, kmult_arrhenius_curve, (bt_soil,), self._lue, "TSOIL", "Rh/Cbar")
    display_ramp(self._SMSF, rh_over_cbar, upward_ramp_func, (SMSF_min, SMSF_max), self._lue, "SMSF", "Rh/Cbar")

  #Gets user input for what outliers to include and exclude for the use of the RECO optimization process
  #(For the use of the command line interface version of the program)
  def cli_get_input(self):
    choice = -1
    still_choosing = True
    c_list = [True,True,True,True]

    print("Choose which parameters to include or exclude in optimization (all included by default):")
    print("0: Continue with optimization")
    print("1: f_aut")
    print("2: b_tsoil")
    print("3: SMSF_min")
    print("4: SMSF_max")
    print("9: View all parameter states (True = included, False = excluded)")

    while(still_choosing):
      try:
        choice = int(input("Which do you choose? (0-9): "))
      except TypeError:
        choice = -1

      if(choice == 0):

        still_choosing = False

      elif(choice > 0 & choice <= 8):

        c_list[choice-1] = not c_list[choice-1]

      elif(choice == 9):

        print("f_aut:",c_list[0],"\nb_tsoil:",c_list[1],"\nSMSF_min:",c_list[2],"\nSMSF_max:",c_list[3])

      else:

        print("Invalid choice, please try again (0-9): ")

      return c_list
