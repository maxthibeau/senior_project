from funcs.ramp_func import *

def calc_e_mult(vpd, vpd_min_max, tmin, tmin_min_max, smrz, smrz_min_max, ft_mult):
  # Equation 6
  return ramp_func(vpd, vpd_min_max) * ramp_func(tmin, tmin_min_max) * ramp_func(smrz, smrz_min_max) * ft_mult

def calc_gpp(fpar, par, epsilon_max, e_mult):
  # Equation 5
  return (fpar * par) * epsilon_max * e_mult
