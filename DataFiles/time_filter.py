# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 09:48:50 2020

@author: The Skyentists
"""

import sys
from os import listdir

class Time_Filter:
  
  #Initiates the Time_Filter class. 
  #Takes in a path to a folder of flux station data files(csv) as a parameter.
  def __init__(self,csv_folder_path):
    
    self.csv_folder_path = csv_folder_path
  
  #Changes the path of the csv_folder thats going to be used
  def set_path(self):
    
    self.csv_folder_path = input("Please specify a folder path here: ")
  
  #Combines all flux tower data into one csv based on a range from the start_year to the end_year into
  #one csv file.
  def create_filtered_file(self,start_year,end_year):
    
    print("Starting...")
    file_list = listdir(self.csv_folder_path)
    
    output_file_name = "compiled_fluxnet_" + str(start_year) + "_" + str(end_year)
    output_file_temp = output_file_name + ".csv"
    output_int = 0
    
    while(self.check_folder(output_file_temp)):
      output_int += 1
      output_file_temp = output_file_name + "_" + str(output_int) + ".csv"
    
    output_file_name = output_file_temp
    
    output_file = open(output_file_name,"w+")
    
    for i in file_list:
      
      print("Current file:",i)
      with open(self.csv_folder_path+"/"+i) as f:
        
        line_list = f.readlines()
        
        for l in line_list:
          line = l.split(',')
          
          if(line[0] != "year"):
            
            if(int(line[0]) >= start_year & int(line[0]) <= end_year):
              output_file.write(l)
            
    output_file.close()
    print("Done")
  
  #Checks the folder for files with the same name as the given file
  #returns true if a file with the same name is found and false otherwise
  def check_folder(self,file):
    file_list = listdir()
    
    if(file in file_list):
      return True
    else:
      return False

#Takes 3 arguments at command line: path, start_year, end_year
def main(argv):
  
  file_filter = Time_Filter(argv[0])
  file_filter.create_filtered_file(int(argv[1]),int(argv[2]))

if __name__ == '__main__':
  main(sys.argv[1:])        
          
    
  

