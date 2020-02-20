# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:36:05 2020

@author: The Skyentists
"""
import sys
from os import listdir
from gpp.py import GPP
from reco.py import RECO
from ramp.py import Ramp

class CLI:
  
  def __init__(self):
    pass
  
  #Displays the intro, gets user input to continue
  def intro(self):
    print("NTSG calibration software. Developed by the Skyentists")
    any_key = input("Press any key to continue....")
    
  #Gets a config file from the user and returns the filename
  def config_file_select(self):
    config_file = input("Please enter a path for the config file you would like to use.")
    try:
      temp_file_test = open(config_file)
    except IOError:
      print("File not found, please try again")
      config_file = self.file_select()
    
    temp_file_test.close()
    
    return config_file
  
  #Gets a outputfile name from the user and returns the filename with the HDF5 extension
  def output_file_select(self):
    output_file = input("Please enter a name for your output file (Preferred format: [PFTname][date], do not include file extension)")
    
    output_file = output_file + ".HDF5"
    
    file_in_folder = self.check_folder(output_file)
    if(file_in_folder):
      choice = input("File already exists, do you wish to overwrite it? (y/n)")
      if(choice == "y"):
        return output_file
      else:
        return self.output_file_select
    else:
      return output_file
  
  #Takes in a list of pft names and has the user choose which pft they would like to use
  #Returns their choice of pft
  def select_pft(self,pft_list):
    pft_num = 0
    print("Please enter a pft from the list below:")
    for p in pft_list:
      pft_num += 1
      print(pft_num,":",p)
    
    current_pft = input("Enter your choice here: ")
    
    if(current_pft not in pft_list):
      print("PFT not found, please try again\n")
      return self.select_pft
    
    return current_pft
      
  #Takes in parameters used for smoothing data and displaying the smoothed data
  #Returns the data that has been smoothed
  #Due to change
  def smooth_outliers(self,val_list,val_name):
    self.display_smoothing(val_list,val_name+" Before Outlier Smoothing")
    smoothed_data = val_list
    still_smoothing = True
    window_size = 0
    while(still_smoothing):
      print("Which method of smoothing would you like to use? (Enter a number 1-5)")
      print("1: flat")
      print("2: hanninghamming")
      print("3: bartlett")
      print("4: blackman")
      print("5: Done Smoothing")
      try:
        choice = int(input("Enter your choice here"))
      except TypeError:
        choice = -1
      
      if(choice > 0 & choice <= 4):
        window_size = self.window_size_select()
      
      if(choice == 1):
        smoothed_data = self.smooth_data(smoothed_data,1,window_size)
      elif(choice == 2):
        smoothed_data = self.smooth_data(smoothed_data,2,window_size)
      elif(choice == 3):
        smoothed_data = self.smooth_data(smoothed_data,3,window_size)
      elif(choice == 4):
        smoothed_data = self.smooth_data(smoothed_data,4,window_size)
      elif(choice == 5):
        still_smoothing = False
      else:
        print("Invalid input, please try again.\n")
    
    self.display_smoothing(smoothed_data,val_name+" After Outlier Smoothing")    
    return smoothed_data
  
  #Takes in the ramp functions and displays them
  #User chooses whether or not they want to display the optional 4th ramp
  #Due to change
  def show_gpp_ramps(self, ramp_1, ramp_2, ramp_3, op_ramp_4):
    deciding = True
    self.display_ramp(ramp_1) #Change later
    self.display_ramp(ramp_2) #Change later
    self.display_ramp(ramp_3) #Change later
    
    choice = input("Display GPP vs emult graph? (y/n)")
    
    while(deciding):
      if(choice == "y"):
        self.display_ramp(op_ramp_4) #Change later
        deciding = False
      elif(choice == "n"):
        deciding = False
      else:
        print("Invalid option, please try again")
  
  #Takes in an object from the GPP class and uses the cli function it has for optimization parameter selection
  #Returns a list of choices for the parameters (Boolean)
  def select_optimization_parameters_gpp(self,gpp_object):
    parameter_list = gpp_object.cli_get_input()
    
    return parameter_list
  
  #Takes in the 8 ramp functions that are provided after the optimization process to displays them
  #Returns the users choice for whether or not they want to redisplay the GPP ramps
  #Due to change
  def gpp_difference_after_optimization(self, ramp_1, ramp_2, ramp_3, ramp_4, ramp_5, ramp_6, ramp_7, ramp_8):
    self.display_ramp(ramp_1) #Change later
    self.display_ramp(ramp_2) #Change later 
    self.display_ramp(ramp_3) #Change later
    self.display_ramp(ramp_4) #Change later
    self.display_ramp(ramp_5) #Change later
    self.display_ramp(ramp_6) #Change later
    self.display_ramp(ramp_7) #Change later
    self.display_ramp(ramp_8) #Change later
    
    deciding = True
    choice = ""
    while(deciding):
      choice = input("Redisplay GPP ramp functions? (y/n) ")
      
      if(choice == "y" | choice == "n"):
        deciding = False
      else:
        print("Invalid choice, please try again")
    
    return choice
  
  #Takes in an object from the RECO class and uses its function for setting prh and pk
  #Returns the reco object after running the function
  def enter_prh_and_pk(self, reco_object):
    reco_object.set_prh_and_pk()
    
    return reco_object
  
  #Takes in 3 ramp functions to display and a user chooses whether or not they want to see the optional 3rd ramp
  #Due to change
  def show_reco_ramps(self,ramp_1, ramp_2, op_ramp_3):
    self.display_ramp(ramp_1) #Change later
    self.display_ramp(ramp_2) #Change later
    
    deciding = True
    while(deciding):
      choice = input("Would you like to display rh/C vs kmult? (y/n) ")
      
      if(choice == "y"):
        deciding = False
        self.display_ramp(op_ramp_3) #Change later
      elif(choice == "n"):
        deciding = False
      else:
        print("Invalid choice, please try again")
        
  #Takes in an object from the RECO class and runs its cli function for parameter selection
  #Returns a list of choices for each parameter (Boolean)
  def select_optimization_parameters_reco(self,reco_object):
    parameter_list = reco_object.cli_get_input()
    
    return parameter_list
  
  #Takes in the ramp functions that are provided after the RECO optimization process and displays them
  #Returns the user's choice for if they want to redisplay the RECO ramp functions
  #Due to change
  def reco_differences_after_optimization(self,ramp_1,ramp_2,ramp_3,ramp_4):
    self.display_ramp(ramp_1) #Change later
    self.display_ramp(ramp_2) #Change later
    self.display_ramp(ramp_3) #Change later
    self.display_ramp(ramp_4) #Change later
    
    deciding = True
    choice = ""
    while(deciding):
      choice = input("Would you like to display RECO ramp functions? (y/n)")
      if(choice == "y" | choice == "n"):
        deciding = False
      else:
        print("Invalid input, please try again")
        
    return choice
  
  #Displays graph for estimated SOC vs calculated SOC
  #Due to change
  def estimated_vs_calculated_soc(self,graph):
    self.display_ramp(graph) #Change later
  
  #Gets user input for how many iterations of the simulation they would like to run
  #Returns the number of simulations the user chose
  def specify_number_of_iterations(self):
    num_of_iterations = 1
    
    try:
      num_of_iterations = int(input("Please enter the number of iterations you want to run: "))
    except TypeError:
      num_of_iterations = 0
      
    if(num_of_iterations <= 0):
      print("Invalid number, please try again")
      num_of_iterations = self.specify_number_of_iterations
    
    return num_of_iterations
  
  #Displays the results of the simulation
  def show_results_of_sim(self,r_value,gpp_rmse,reco_rmse,nee_rmse):
    print("Simulation Complete!")
    print("Pearson's R-Value:",r_value)
    print("GPP RMSE:",gpp_rmse)
    print("RECO RMSE:",reco_rmse)
    print("NEE RMSE",nee_rmse)
  
  #Checks a folder for a specific file
  #Returns true if it exists, false otherwise
  def check_folder(self,file):
    file_list = listdir()
    
    if(file in file_list):
      return True
    else:
      return False
  
  #Gets the user's input for a float that is greater than 0 for the window size
  #Returns that window size
  def window_size_select(self):
    window_size = 0
    try:
      window_size = float(input("Please select a window size.(float greater than 0)"))
    except TypeError:
      window_size = 0
      
    if(window_size <= 0):
      print("Invalid window size, please try again.")
      window_size = self.window_size_select()
      
    return window_size
  
  #Placeholder function stubs for later
  def display_smoothing(self, val_list):
    pass
  
  def smooth_data(self, val_list, smoothing_type, window_size):
    pass
  
  def display_ramp(self, ramp_data):
    pass
