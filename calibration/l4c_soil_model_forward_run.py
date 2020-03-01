# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 05:42:33 2020

@author: The Skyentists
"""
import sys
import numpy as np
import h5py
from MeteorologicalInput.py import MeteorlogicalInput

class L4C_Soil_Model_Forward_Run:
  
  def __init__(self, ropt, kstr, krec, fmet, fstr, faut, gpp1km, kmult1km, litterfall, cmet0, cstr0, crec0, ns, days, input_object_m):
    self.CELLS = 81
    
    self.ropt = ropt
    self.kstr = kstr
    self.krec = krec
    self.fmet = fmet
    self.fstr = fstr
    self.faut = faut
    self.ns = ns
    self.days = days
    self.input_object_m = input_object_m
    
    self.gpp1km = gpp1km
    self.kmult1km = kmult1km
    
    self.litterfall = litterfall
    self.pft = input_object_m.pft_grids()
    
    self.rh1 = np.zeros([self.ns,self.CELLS])
    self.rh2 = np.zeros([self.ns,self.CELLS])
    self.rh3 = np.zeros([self.ns,self.CELLS])
    
    self.cbar0 = np.zeros([self.ns])
    
    self.dc1 = np.zeros([self.ns,self.CELLS])
    self.dc2 = np.zeros([self.ns,self.CELLS])
    self.dc3 = np.zeros([self.ns,self.CELLS])
    
    self.c1 = cmet0
    self.c2 = cstr0
    self.c3 = crec0
  
  def num_valid_pft(self, selected_pft):
    valid_per_site = np.zeros([self.ns])
    i_count = 0
    for site in self.pft:
      p_count = 0
      for cell in site:
        if(cell == selected_pft):
          p_count += 1
      
      valid_per_site[i_count] = p_count
    
    return valid_per_site
  
  def run_model(self):
    dc_total = np.zeros([self.ns, self.CELLS])
    tolerance = np.zeros([self.ns, self.CELLS])
    track = np.array([np.zeros([self.days,self.ns,self.CELLS]),
                      np.zeros([self.days,self.ns,self.CELLS]),
                      np.zeros([self.days,self.ns,self.CELLS]),
                      np.zeros([self.days,self.ns,self.CELLS]),
                      np.zeros([self.days,self.ns,self.CELLS]),
                      np.zeros([self.days,self.ns,self.CELLS])])
    for d in self.days:
      self.cbar0 = 0*self.cbar0
      
      self.rh1 = self.ropt * self.kmult1km[d] * self.c1
      self.rh2 = self.ropt * self.kstr * self.kmult1km[d] * self.c2
      self.rh3 = self.ropt * self.krec * self.kmulst1km[d] * self.c3
    
      self.cbar0 = self.cbar0 + (self.ropt * self.c1) + (self.ropt * self.krec * self.c3)
      
      self.dc1 = (self.litterfall * self.fmet) - self.rh1
      self.dc2 = (self.litterfall * (1 - self.fmet)) - self.rh2
      self.dc3 = (self.fstr * self.rh2) - self.rh3
      
      self.rh2 = self.rh2 * (1-self.fstr)
      
      self.c1 = self.c1 + self.dc1
      self.c2 = self.c2 + self.dc2
      self.c3 = self.c3 + self.dc3
      
      for n in range(self.ns):
        for c in range(self.CELLS):
          dc_total[n,c] = self.dc1[n,c] + self.dc2[n,c] + self.dc3[n,c]
      
      tolerance = tolerance + dc_total
      
      track[0,d] = self.rh1 +self.rh2 + self.rh3 #rh_total
      track[1,d] = self.c1 + self.c2 + self.c3 #c_total
      track[2,d] = self.faut * self.gpp1km[d] #ra
      track[3,d] = track[2,d] + track[0,d] #RECO
      track[4,d] = track[3,d] - self.gpp1km[d] #NEE
      track[5,d] = tolerance
    
    return track, self.c1, self.c2, self.c3, self.cbar0
      
      
      
      
      
      
      