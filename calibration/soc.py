# -*- coding: utf-8 -*-
"""
Created on Thurs Mar 5 2020

@author: The Skyentists
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import math
from AnalyticalModelSpinUp import *
from NumericalModelSpinUp import *
from RampFunctions import *
from scipy import stats

#The SOC class will hold variables and functions used in the SOC estimation process
class SOC:

  #Initializes the SOC class
  def __init__(self,pft,bplut,flux_towers,kmult_365,npp_365):
      self.fmet = float(bplut[pft,'fmet'])
      self.fstr = float(bplut[pft,'fstr'])
      self.ropt = float(bplut[pft,'kopt'])
      self.kstr = float(bplut[pft,'kstr'])
      self.krec = float(bplut[pft,'kslw'])
      self.kmult_365 = kmult_365 #from analytical model spin up
      self.npp_365 = npp_365 # from analytical model spin up
      self.avg_litterfall = 0.0 #updated in calc_sigmas()
      self.towers = flux_towers
      self.sigmas = self.calc_sigmas()
      self.beta_soc = self.calc_beta_soc() #only 1 soc for each different fmet,fstr,ropt,kstr,krec
      self.estimated_soc = self.calc_estimate()
      print("Calculated SOC: ",self.estimated_soc)
      #self.actual_soc = actual_soc #TODO: Change to actual soc calc for each tower
      #self.display_graph()

  def calc_sigmas(self): #from 10c in Procedure 3.3 in Requirements Draft Doc
      sigmas = []
      conv_1 = (1/len(self.towers))
      npp_star = 0.0
      for flux in self.towers: #for each tower
          #tower = self.towers[flux]
          kmult_star = 0.0
          for k in self.kmult_365:
             if not math.isnan(k):
                 kmult_star += k

          for n in self.npp_365:
             if not math.isnan(n):
                 npp_star += n
          conv_2 = npp_star/kmult_star
          sigma = conv_1 * conv_2
          sigmas.append(sigma)
      self.avg_litterfall = npp_star/(len(self.npp_365)) #avg litterfall for npps
      return sigmas

  def calc_beta_soc(self): #from 10d in Procedure 3.3 in Requirements Draft Doc
        s = 0.001 #scaling param, results in vals with units of: (kg*C)/(m^2)
        part_1 = (1 - self.fmet)/self.kstr
        part_2 = (self.fstr*(1 - self.fmet))/self.krec
        big_part = (self.fmet + part_1 + part_2)
        soc = s * big_part/self.ropt
        return soc #one for each bplut

  def calc_estimate(self): # y values for SOC estimation
        arr = []
        for i in range(len(self.towers)): #for each tower: sigma * Beta_soc
            val = self.sigmas[i] * self.beta_soc
            arr.append(val)
        return arr

  def get_litterfall(self):
      return self.avg_litterfall

  def display_graph(self):
         x = self.actual_soc
         y = self.estimated_soc
         self.r_val = stats.pearsonr(x,y) #for display of r-val on graph
         text = "Pearson's r-val = "+round(self.r_val,2)
         ax = self.figure.add_subplot(111)
         ax.clear()
         ax.scatter(x,y)
         ax.set_title("SOC Estimation")
         ax.set_xlabel("IGBP SOC [kg C m^-2]") #ground truth SOC
         ax.set_ylabel("Estimated SOC [kg C m^-2]") #estimated/calculated SOC
         ax.text(0.05, 0.95,text,fontsize=14,transform=ax.transAxes,verticalalignment='top',bbox=props)
         ax.show()
