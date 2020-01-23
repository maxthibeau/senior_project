# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 22:44:33 2020

@author: The Skyentists
"""

import sys
import matplotlib.pyplot as plt
import numpy as np

#The RECO class will hold variables and functions used in the RECO optimization process
class RECO:
    
    #Initializes the RECO class
    def __init__(self,reco_val,prh,pk,f_aut,b_tsoil,SMSF_min, SMSF_max):
        self.reco_val = reco_val
        self.prh = prh
        self.pk = pk
        self.f_aut = f_aut
        self.b_tsoil = b_tsoil
        self.SMSF_min = SMSF_min
        self.SMSF_max = SMSF_max
    
    #Calculates RECO (if not already given)
    def calc_reco(self, gpp, nee):
        pass
    
    #Sets prh and pk
    def set_prh_and_pk(self):
        pass
    
    #Calculates C_bar
    def calc_cbar(self):
        pass
    
    #Calculates K_mult
    def calc_kmult(self):
        pass
    
    #Calculates the ramp function of TSOIL (f(TSOIL))
    def calc_TSOIL(self,x):
        pass
    
    #Calculates the ramp function of SMSF (f(SMSF))
    def calc_SMSF(self,x):
        pass
    
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
        