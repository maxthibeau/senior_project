from ramp_func import *

def arrhenius_curve(self, beta_t_soil, t_soil):
  # Equation 10
  # NOTE: where are magic numbers coming from?
  return np.exp(beta_t_soil *  (1 / 66.02 - 1 / (t_soil - 227.13) ) ) 

def k_mult(t_soil, smsf):
  # equation_9
  return arrhenius_curve (t_soil) * ramp_func(smsf)

def reco(f_aut, gpp, k_mult, c_bar):
  # Equation 11
  return f_aut * gpp, + k_mult * c_bar
