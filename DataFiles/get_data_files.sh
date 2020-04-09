#!/bin/bash

wget http://files.ntsg.umt.edu/data/SKYentists/L4C_calibration_inputs/SMAP_L4_C_mdl_Vv3040_001_NRv41_smapMergedCalVal.h5 &
wget http://files.ntsg.umt.edu/data/SKYentists/L4C_calibration_inputs/Fluxnet2015_flux_tower_station_data.zip &
wget http://files.ntsg.umt.edu/data/SKYentists/L4C_calibration_inputs/L4_C_input_NRv72_Vv4xxxx_smapMergedCalVal.h5 &
wget http://files.ntsg.umt.edu/data/SKYentists/L4C_calibration_inputs/202002/calibSites_Natv72.csv &
wget http://files.ntsg.umt.edu/data/SKYentists/L4C_calibration_inputs/igbp_soc_M09smapMergedCalVal.flt32 &

wait

touch flux_towers_to_exclude.txt
unzip Fluxnet2015_flux_tower_station_data.zip 
