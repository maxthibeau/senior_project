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
    def __init__(self,gpp_val,lue,VPD_min,VPD_max,
                 SMRZ_min,SMRZ_max,TMIN_min,TMIN_max,FT_mult):
        self.gpp_val = gpp_val
        self.lue = lue
        self.VPD_min = VPD_min
        self.VPD_max = VPD_max
        self.SMRZ_min = SMRZ_min
        self.SMRZ_max = SMRZ_max
        self.TMIN_min = TMIN_min
        self.TMIN_max = TMIN_max
        self.FT_mult = FT_mult
    
    #Calculates GPP (if not already given)
    def calc_gpp(self):
        pass
    
    #Calculates APAR with inputs PAR and FPAR (APAR = PAR X FPAR)
    def calc_APAR(self, PAR, FPAR):
        pass
    
    #Calculates E_mult (E_mult = f(VPD)*f(TMIN)*f(SMRZ)*FT_mult)
    def calc_emult(self):
        pass
    
    #Calculates the ramp function of SMRZ (f(SMRZ))
    def calc_ramp_SMRZ(self,x):
        pass
    
    #Calculates the ramp function of TMIN (f(TMIN))
    def calc_ramp_TMIN(self,x):
        pass
    
    #Calculates the ramp function of VPD (f(VPD))
    def calc_ramp_VPD(self,x):
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
            except TypeError:
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
    

        

