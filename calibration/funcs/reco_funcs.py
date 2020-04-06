from funcs.ramp_func import *

def kmult(t_soil, smsf, bt_soil, smsf_min, smsf_max):
  # equation_9
  return kmult_arrhenius_curve (t_soil, bt_soil) * upward_ramp_func(smsf, (smsf_min, smsf_max))

def reco(gpp, t_soil, smsf, c_bar, f_aut, bt_soil, a, b, smsf_min, smsf_max):
  # Equation 11
  return f_aut * gpp + arrhenius_curve(t_soil, (bt_soil, a, b)) * upward_ramp_func(smsf, (smsf_min, smsf_max)) * c_bar

# for when kmult needs to be filtered on the reco optimization process
def reco(gpp, kmult, c_bar, f_aut):
  return f_aut * gpp * kmult
