# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 08:38:29 2020

@author: The Skyentists
"""

import sys
import matplotlib.pyplot as plt
import numpy as np

#The GPP class will hold variables and functions used in the GPP optimization process
class GPP:

  #Initializes the GPP class
  def __init__(self,pft,bplut,VPD_val,SMRZ_val,TMIN_val,Par_val,FPAR_val): #,FT_mult
    # GPP: 5=LUEmax, 6=Tmin_min_K, 7=Tmin_max_K, 8=VPD_min_Pa, 9=VPD_max_Pa, 10=SMrz_min, 11=SMrz_max, 12=FT_min, 13=FT_max
    #from inputs
    self.Par_val = Par_val
    self.FPAR_val = FPAR_val
    self.VPD_val = VPD_val
    self.SMRZ_val = SMRZ_val
    self.TMIN_val = TMIN_val
    #from bplut
    self.lue = bplut[pft][5]
    self.VPD_min = bplut[pft][8] #in Pa
    self.VPD_max = bplut[pft][9]
    self.SMRZ_min = bplut[pft][10]
    self.SMRZ_max = bplut[pft][11]
    self.TMIN_min = bplut[pft][6] #in K
    self.TMIN_max = bplut[pft][7]
    self.FT_mult_min = bplut[pft][12]
    self.FT_mult_max = bplut[pft][13]
    self.gpp_val = self.calc_gpp()

  #Calculates GPP (if not already given)
  def calc_gpp(self):
    APAR = self.calc_APAR(self.Par_val,self.FPAR_val)
    gpp = APAR * self.lue * self.calc_emult() # self.lue is the same as Emax
    return gpp
  #Calculates APAR with inputs PAR and FPAR (APAR = PAR X FPAR)
  def calc_APAR(self, PAR, FPAR):
    apar = PAR * FPAR
    return apar

  #Calculates E_mult (E_mult = f(VPD)*f(TMIN)*f(SMRZ)*FT_mult)
  def calc_emult(self):
    FT_mult = self.FT_mult_min
    E_mult = self.calc_ramp_VPD(self.VPD_val) * self.calc_ramp_TMIN(self.TMIN_val) * self.calc_ramp_SMRZ(self.SMRZ_val) * FT_mult
    return E_mult

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
