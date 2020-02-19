import sys
import csv
from input_files import ConfigFile
from PFTSelector import *
from gpp import *
from reco import *

def main(argv):
  if len(argv) < 1:
    print ("usage: <config file>")
    exit(1)
  config_fname = argv[0]
  config_file = ConfigFile.ConfigFile(config_fname)
  meteor_input = config_file.meteorological_input()
  flux_tower_data = config_file.flux_tower_data()
  reference_input = config_file.reference_input()
  pft = PFTSelector.select_pft(meteor_input)

  tower_sites = meteor_input.sites_claimed_by_pft(pft)
  flux_lat_long = meteor_input.lat_long()
  flux_tower_data = flux_tower_data.set_coords(flux_lat_long)

  flux_tower_data_by_pft = flux_tower_data.take(tower_sites)
  # print(reference_input.subset_data(['EC', 'frozen_area']))
  # meteor_tower_data_by_pft = meteor_input.take(tower_sites)
  # reference_data_by_pft = freference_data.take(tower_sites)

  # pft_data = PFT(pft_selected, meteor_input, reference_input)

  former_bplut = config_file.reference_bplut_table()
  bplut = former_bplut.load_current()
  pft = int(pft)
  # GPP
  VPD = meteor_input.subset_data_by_pft(['MET','vpd'],pft,0) #meterological input MET (vpd) array
  SMRZ = meteor_input.subset_data_by_pft(['MET','smrz'],pft,0) #meterological input MET (smrz) array
  TMIN = meteor_input.subset_data_by_pft(['MET','tmin'],pft,0) #meterological input MET (tmin) array
  FPAR = meteor_input.subset_data_by_pft(['MOD','fpar'],pft,0) #meterological input MOD (fpar)
  PAR = get_Par(flux_tower_data_by_pft) #flux tower input (par)
  gpp_calcs = GPP(pft,bplut,VPD,SMRZ,TMIN,PAR,FPAR)
  former_bplut.after_optimization(pft,[2,5,8,10,11]) #CHANGE ARRAY
  #RECO
  Tsoil = meteor_input.subset_data_by_pft(['MET','tsoil'],pft,0) #meterological input MET (tsoil)
  SMSF = meteor_input.subset_data_by_pft(['MET','smsf'],pft,0) #meterological input MET (smsf)
  kmult_365 = 0.0 #from forward run
  npp_365 = 0.0 #from forward run
  #reco_calcs = RECO(pft,bplut,gpp_calcs,Tsoil,SMSF,kmult_365,npp_365)
  #former_bplut.after_optimization(pft,[14,17,20]) #CHANGE ARRAY

def get_Par(files):
    PARs = []
    for x in range(len(files)):
        flux_tower = files[x]
        flux_tower = flux_tower[:47]+'/'+flux_tower[47:]
        file = open(flux_tower)
        lines = csv.reader(row for row in file if not row.startswith('#'))
        tower_par = []
        total_par = 0
        for row in lines:
            par = row[11]
            total_par = 0
            if(par != 'NaN' and par != 'par'):
                tower_par.append(par)
                total_par += float(par)
        if(len(tower_par) != 0):
            par_val = total_par/len(tower_par)
            PARs.append(par_val)
        file.close()
    return PARs

if __name__ == "__main__":
  main(sys.argv[1:])
