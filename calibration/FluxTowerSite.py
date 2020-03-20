from funcs.ramp_func import *

class FluxTowerSite:
  def __init__(self,name,vars):
    self.name = name
    self.year = int(vars[0])
    self.month = int(vars[1])
    self.day = int(vars[2])
    self.t = int(vars[3])
    self.nee = float(vars[4])
    self.gpp = float(vars[5])
    self.reco = float(vars[6])
    self.swc = float(vars[7])
    self.ts = float(vars[8])
    self.vpd = float(vars[9])
    self.ta = float(vars[10])
    self.par = float(vars[11])
    self.rad = float(vars[12])
    self.precip = float(vars[13])

######################
# Getters
######################

  def get_name(self):
    return self.name
  def get_year(self):
    return self.year
  def get_month(self):
    return self.month
  def get_day(self):
    return self.day
  def get_t(self):
    return self.t
  def get_nee(self):
    return self.nee
  def get_gpp(self):
    return self.gpp
  def get_reco(self):
    return self.reco
  def get_swc(self):
    return self.swc
  def get_ts(self):
    return self.ts
  def get_vpd(self):
    return self.vpd
  def get_ta(self):
    return self.ta
  def get_par(self):
    return self.par
  def get_rad(self):
    return self.rad
  def get_precip(self):
    return self.precip

#######################
# Setters
#######################

  def set_name(self,val):
    self.name = val
  def set_year(self,val):
    self.year = val
  def set_month(self,val):
    self.month = val
  def set_day(self,val):
    self.day = val
  def set_t(self,val):
    self.t = val
  def set_nee(self,val):
    self.nee = val
  def set_gpp(self,val):
    self.gpp = val
  def set_reco(self,val):
    self.reco = val
  def set_swc(self,val):
    self.swc = val
  def set_ts(self,val):
    self.ts = val
  def set_vpd(self,val):
    self.vpd = val
  def set_ta(self,val):
    self.ta = val
  def set_par(self,val):
    self.par = val
  def set_rad(self,val):
    self.rad = val
  def set_precip(self,val):
    self.precip = val

#########################
# Calc_and_Setters
#########################

def calc_and_set_gpp(self,fpar, par, epsilon_max, e_mult):
  self.gpp = (fpar * par) * epsilon_max * e_mult

def calc_and_set_k_mult(self,f_t_soil, f_smsf):
  self.kmult = f_t_soil * f_smsf

#Note GPP must be set first!!!
def calc_and_set_npp(self,f_aut):
  self.npp = self.gpp - (f_aut * self.gpp)

