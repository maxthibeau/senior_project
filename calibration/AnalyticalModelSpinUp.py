import numpy as np
import math

class AnalyticalModelSpinUp():

  def __init__(self, k_mults, towers_gpp, f_met, f_str, r_opt, k_str, k_rec, fraut):

    self._npps = self.calc_npp(towers_gpp,fraut)

    self._c_mets = []
    self._c_strs = []
    self._c_recs = []
    self._c_bars = []
    self._summed_kmults = []
    self._summed_npps = []

    for k_mult, npp in zip(k_mults, self._npps):

      k_mult_sum = np.sum(k_mult, axis = 0)
      npp_sum = np.sum(npp, axis = 0)

      self._summed_kmults.append(k_mult_sum)
      self._summed_npps.append(npp_sum)

      c_met = f_met * npp_sum/(r_opt * k_mult_sum)
      c_str = (1 - f_met) * npp_sum / (r_opt * k_str * k_mult_sum)
      c_rec = f_str * k_str * c_str / k_rec
      c_bar = (r_opt * c_met) + (k_str * (r_opt * c_str)) + (k_rec * (r_opt * c_rec) )

      self._c_mets.append(c_met)
      self._c_strs.append(c_str)
      self._c_recs.append(c_rec)
      self._c_bars.append(c_bar)

  def calc_npp(self,tower_gpp,fraut):
      npps = []
      for i in tower_gpp:
          npp_calc = []
          for val in i:
              if not math.isnan(val):
                  npp = val - (fraut * val)
                  npp_calc.append(npp)
          npps.append(npp_calc)
      return npps

  def c_mets(self):
    return self._c_mets

  def c_strs(self):
    return self._c_strs

  def c_recs(self):
    return self._c_recs

  def c_bars(self):
    return self._c_bars

  def summed_kmults(self):
    return self._summed_kmults

  def summed_npps(self):
    return self._summed_npps

  def get_npps(self):
    return self._npps

# testing
def main():
  k_mults = np.zeros((1, 365, 81)) + 1
  npps = np.zeros((1, 365, 81)) + 2
  f_met = .5
  f_str = 1
  r_opt = 1
  k_str = 1
  k_rec = 1
  annie = AnalyticalModelSpinUp(k_mults, npps, f_met, f_str, r_opt, k_str, k_rec)
  print(" c_mets: ",annie.c_mets(),"\n\n","c_strs: ", annie.c_strs(),"\n\n","c_recs: ", annie.c_recs(),"\n\n","c_bars: ", annie.c_bars())

if __name__ == "__main__":
  main()
