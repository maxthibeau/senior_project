from funcs.ramp_func import *
def gpp(fpar, par, vpd, tmin, smrz, tsurf, lue, vpd_min, vpd_max, tmin_min, tmin_max, smrz_min, smrz_max, ft_mult_frozen, ft_mult_thawed):
  vpd_ramp = downward_ramp_func(vpd, (vpd_min, vpd_max))
  tmin_ramp = upward_ramp_func(tmin, (tmin_min, tmin_max))
  smrz_ramp = upward_ramp_func(smrz, (smrz_min, smrz_max))

  ft_mult = np.piecewise(tsurf, [tsurf < 273, tsurf >= 273], [ft_mult_frozen, ft_mult_thawed])

  e_mult = vpd_ramp * tmin_ramp * smrz_ramp * ft_mult

  return fpar * par * lue * e_mult

# useful for when bounds are set on APAR
def gpp_apar(apar, vpd, tmin, smrz, tsurf, lue, vpd_min, vpd_max, tmin_min, tmin_max, smrz_min, smrz_max, ft_mult_frozen, ft_mult_thawed):
  vpd_ramp = downward_ramp_func(vpd, (vpd_min, vpd_max))
  tmin_ramp = upward_ramp_func(tmin, (tmin_min, tmin_max))
  smrz_ramp = upward_ramp_func(smrz, (smrz_min, smrz_max))

  ft_mult = np.piecewise(tsurf, [tsurf < 273, tsurf >= 273], [ft_mult_frozen, ft_mult_thawed])

  e_mult = vpd_ramp * tmin_ramp * smrz_ramp * ft_mult

  return apar * lue * e_mult

def emult(self, vpd, tmin, smrz, tsurf, vpd_min, vpd_max, tmin_min, tmin_max, smrz_min, smrz_max, ft_mult_frozen, ft_mult_thawed):
  vpd_ramp = downward_ramp_func(vpd, (vpd_min, vpd_max))
  tmin_ramp = upward_ramp_func(tmin, (tmin_min, tmin_max))
  smrz_ramp = upward_ramp_func(smrz, (smrz_min, smrz_max))

  ft_mult = np.piecewise(tsurf, [tsurf < 273, tsurf >= 273], [ft_mult_frozen, ft_mult_thawed])

  e_mult = vpd_ramp * tmin_ramp * smrz_ramp * ft_mult

  return emult
