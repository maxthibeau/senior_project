# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 22:44:33 2020

@author: The Skyentists
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import math
from AnalyticalModelSpinUp import *
from NumericalModelSpinUp import *

#The RECO class will hold variables and functions used in the RECO optimization process
class RECO:

  #Initializes the RECO class
  def __init__(self,pft,bplut,gpp_val,Tsoil_val,SMSF_val,kmult_365,npp_365):
    # RECO: 14=SMtop_min, 15=SMtop_max, 16=Tsoil_beta0, 17=Tsoil_beta1, 18=Tsoil_beta2, 19=fraut, 20=fmet, 21=fstr, 22=kopt, 23=kstr, 24=kslw
    #from input
    self.kmult_365 = kmult_365
    self.npp_365 = npp_365
    self.Tsoil_val = Tsoil_val
    self.SMSF_val = SMSF_val
    self.gpp_val = gpp_val
    #from user
    self.prh = 0
    self.pk = 0
    self.set_prh_and_pk()
    #from BPLUT
    self.f_aut = bplut[pft][19]
    self.b_tsoil = (bplut[pft][16]+bplut[pft][17]+bplut[pft][18])/3
    self.SMSF_min = bplut[pft][14]
    self.SMSF_max = bplut[pft][15]
    self.fmet = bplut[pft][20]
    self.fstr = bplut[pft][21]
    self.ropt = bplut[pft][22]
    self.kstr = bplut[pft][23]
    self.krec = bplut[pft][24]
    self.reco_val = self.calc_reco()

  #Calculates RECO (if not already given)
  def calc_reco(self):
    Ra = self.f_aut * self.gpp_val
    kmult = self.calc_kmult()
    Rh = kmult * self.calc_cbar()
    RECO = Ra + Rh
    return RECO

  #Sets prh and pk
  def set_prh_and_pk(self):
    still_choosing = True
    while(still_choosing):
      try:
        prh = float(input("Please specify a Prh: "))
        pk = float(input("Please specify a Pk: "))
      except ValueError:
        prh = -1
        pk = -1

      if(pk <= 1 & pk >= 0 & prh <= 1 & prh >= 0):
        still_choosing = False
      else:
        print("Invalid value: please try again")

    self.prh = prh
    self.pk = pk


  #Calculates C_bar
  def calc_cbar(self):
    fast_pool = (self.fmet * self.npp_365)/(self.ropt * self.kmult_365)
    med_pool = ((1-self.fmet) * self.npp_365)/(self.ropt * self.kstr * self.kmult_365)
    slow_pool = (self.fstr * self.kstr * med_pool) / self.krec
    cbar_0 = (self.ropt * fast_pool) + (self.kstr * self.ropt * med_pool) + (self.krec * self.ropt * slow_pool)
    return cbar_0

  #Calculates K_mult
  def calc_kmult(self):
    K_mult = self.calc_TSOIL() * self.calc_SMSF(self.SMSF_val)
    return K_mult

  #Calculates the ramp function of TSOIL (f(TSOIL))
  def calc_TSOIL(self,x):
    conv = (1/66.02) - (1/(x - 227.13))
    TSOIL = math.exp(self.b_tsoil * conv)
    return TSOIL

  #Calculates the ramp function of SMSF (f(SMSF))
  def calc_SMSF(self,x):
    val = 0
    if(x >= self.SMSF_max):
        val = 1
    elif(x <= self.SMSF_min):
        val = 0
    else:
        val = (x - self.SMSF_min)/(self.SMSF_max - self.SMSF_min)
    return val

  #The RECO optimization function with no input given (All outliers included)
  def optimize_reco(self):
    pass

  #The RECO optimization function with a boolean list of what outliers to include
  #Input order: [f_aut, b_tsoil, SMSF_min, SMSF_max]
  def optimize_reco(self,choice_vector):
    pass

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
