import numpy as np
from AnalyticalModelSpinUp import *
'''
Note: class is not vigorously tested
'''
class NumericalModelSpinUp():

  def __init__(self, gpps_1km, kmults_1km, litterfalls, pfts, r_opt, k_str, k_rec, f_met, f_str, f_aut, analytical_model_spin_up):

    # inputs
    self._gpps_1km = gpps_1km
    self._kmults_1km = kmults_1km
    self._litterfalls = litterfalls
    self._pfts = pfts
    self._r_opt = r_opt
    self._k_str = k_str
    self._k_rec = k_rec
    self._f_met = f_met
    self._f_str = f_str
    self._f_aut = f_aut
    self._anal_model_spin_up = analytical_model_spin_up

    # output
    self._cbar_list = []
    self._c1_list = []
    self._c2_list = []
    self._c3_list = []

    num_iterations = self.set_iterations()
    for i in range(num_iterations):
      self._forward_run()

    print("C_Bar: ",self._cbar_list)
    print("C1 (Slow Pool): ",self._c1_list)
    print("C2 (Medium Pool): ",self._c2_list)
    print("C3 (Fast Pool): ",self._c3_list)

  def _forward_run(self):

    dimensions = self._gpps_1km.shape
    # number of sites
    n_s = dimensions[0]
    days = dimensions[1]
    cells_per_site = dimensions[2]

    # final outputs
    rh_total = np.zeros(dimensions)
    c_total = np.zeros(dimensions)
    ra = np.zeros(dimensions)
    reco = np.zeros(dimensions)
    nee = np.zeros(dimensions)
    tolernace = np.zeros(dimensions)

    # Initialize state matrices that are [Ns x 81] in size with zeros
    rh1 = np.zeros((n_s, cells_per_site))
    rh2 = np.zeros((n_s, cells_per_site))
    rh3 = np.zeros((n_s, cells_per_site))

    dc1 = np.zeros((n_s, cells_per_site))
    dc2 = np.zeros((n_s, cells_per_site))
    dc3 = np.zeros((n_s, cells_per_site))

    # Set the intial pool sizes; these are [Ns x 81] matrices
    c1 = self._anal_model_spin_up.c_mets()
    c2 = self._anal_model_spin_up.c_strs()
    c3 = self._anal_model_spin_up.c_recs()

    tolerance = np.zeros((n_s, cells_per_site))

    # for each day in T days
    for day in range(days):
      cbar0 = np.zeros((n_s, cells_per_site))

      # kmult1km is a [T x Ns x 81] matrix
      rh1 = self._r_opt * self._kmults_1km[:,day,:] * c1
      rh2 = self._r_opt * self._k_str * self._kmults_1km[:,day,:] * c2
      rh3 = self._r_opt * self._k_rec * self._kmults_1km[:,day,:] * c3

      # Accumulate cbar0
      cbar0 = cbar0 + (self._r_opt * c1) + (self._r_opt * self._k_str * c2) + (self._r_opt * self._k_rec * c3)

      # calculate change in each pool (litterfall is [Ns x 81 matrix)
      dc1 = (self._litterfalls * self._f_met) - rh1
      dc2 = (self._litterfalls * (1 - self._f_met)) - rh2
      dc3 = (self._f_str * rh2) - rh3

      # Slight adjustment for "humification"
      dc3 = (self._f_str * rh2) - rh3

      # Accumulate C pools
      c1 = c1 + dc1
      c2 = c2 + dc2
      c3 = c3 + dc3

      # Calculate total change across all 3 pools, explicity by site, 1-km cell
      dc_total = dc1 + dc2 + dc3

      # And we keep track of this fine-scale change as model move forward
      tolerance += dc_total

      # Keep track of state on each day
      rh_total[:,day,:] = rh1 + rh2 + rh3
      c_total[:,day,:] = c1 + c2 + c3
      ra[:,day,:] = self._f_aut * self._gpps_1km[:,day,:]
      reco[:,day,:] = ra[:,day,:] + rh_total[:,day,:]
      nee[:,day,:] = reco[:,day,:] - self._gpps_1km[:,day,:]

    # Keep a record of cpools
    self._c1_list.append(c1)
    self._c2_list.append(c2)
    self._c3_list.append(c3)
    self._cbar_list.append(cbar0)

  def c1_list(self):
    return self._c1_list

  def c2_list(self):
    return self._c2_list

  def c3_list(self):
    return self._c3_list

  def cbar_list(self):
    return self._cbar_list

  def set_iterations(self):
      still_choosing = True
      iterations = -1
      while(still_choosing):
          try:
            iterations = int(input("Please specify the number of iterations (whole number): "))
          except ValueError:
            iterations = 0
          if(iterations > 0):
            still_choosing = False
          else:
            print("Invalid value: please try again")
      return iterations

def main():
  # tuple indexing gotes site, day, and grid loc.
  gpps_1km = np.zeros((2, 2, 81)) + 1
  k_mults_1km = np.zeros((2, 2, 81)) + 1
  npps_1km = np.zeros((1, 2, 81)) + 2
  # average daily litterfall
  litterfalls_1km = np.zeros((1, 81))
  pfts = np.zeros((1, 81))

  f_met = .5
  f_str = 1
  r_opt = 1
  k_str = 1
  k_rec = 1
  f_aut = 1

  annie = AnalyticalModelSpinUp(k_mults_1km, npps_1km, f_met, f_str, r_opt, k_str, k_rec)
  nummy = NumericalModelSpinUp(gpps_1km, k_mults_1km, litterfalls_1km, pfts, r_opt, k_str, k_rec, f_met, f_str, f_aut, annie)

if __name__ == "__main__":
  main()
