import numpy as np
import h5py
from collections import defaultdict
from scipy import stats
from datetime import date
from datetime import timedelta
from datetime import datetime

class MeteorologicalInput():

  def __init__(self, h5_fname):
    self._h5_file = h5py.File(h5_fname, 'r')
    self._pft_grids = self._subset_data(['ANC', 'lc_dom']).T
    self._lat_long = self._subset_data(['SUBSET','site_latlon'])
    self._date_time = self._subset_data(['SUBSET', 'date_time'])
    self._pfts = np.unique(self._pft_grids)
    self._pft_to_claimed_sites = self._find_pft_to_claimed_sites()

    self._VPD = self._subset_data(['MET', 'vpd'])
    self._SMRZ = self._subset_data(['MET', 'smrz'])
    self._SMSF = self._subset_data(['MET','smsf'])
    self._TMIN = self._subset_data(['MET', 'tmin'])
    self._TSURF = self._subset_data(['MET', 'tsurf'])
    self._FPAR = self._subset_data(['MOD', 'fpar'])
    # this data doesn't exist
    #self._PAR = self._subset_data(['MET', 'par'])
    self._TSOIL = self._subset_data(['MET','tsoil'])

    self._meteor_vars = [self._VPD, self._SMRZ, self._SMSF, self._TMIN, self._TSURF, self._TSOIL, self._FPAR] #, self._PAR]

  def pfts(self,first,last):
    return self._pfts[first:last]

  def pft_grids(self):
    return self._pft_grids

  def site_names(self):
    return self._site_names

  def lat_long(self):
    return self._lat_long

  def VPD(self):
    return self._meteor_vars[0]

  def SMRZ(self):
    return self._meteor_vars[1]

  def SMSF(self):
    return self._meteor_vars[2]

  def TMIN(self):
    return self._meteor_vars[3]

  def TSURF(self):
    return self._meteor_vars[4]

  def TSOIL(self):
    return self._meteor_vars[5]

  def FPAR(self):
    return self._meteor_vars[6]

  '''
  def PAR(self):
    return self._meteor_vars[7]
  '''

  def sites_claimed_by_pft(self, pft):
    return self._pft_to_claimed_sites[int(pft)]

  def subset_by_pft(self, tower_sites_claimed_by_pft):
    for i in range(len(self._meteor_vars)):
      self._meteor_vars[i] = self._meteor_vars[i].take(indices = tower_sites_claimed_by_pft, axis = -1)
    self._lat_long = self._lat_long.take(indices = tower_sites_claimed_by_pft, axis = 0)

  def _is_leap_year(self, date):
    return date.year % 4 == 0

  def compute_climatological_year(self, start_date, end_date):
    first_date = datetime(2000, 1, 1)
    assert(start_date >= first_date and end_date <= datetime.now())
    # for every variable in meteorological input
    for var_index in range(len(self._meteor_vars)):
      # 365 day climatology
      var_climatology = [[] for x in range(365)]
      date = start_date
      day_inc = timedelta(days=1)
      # loop through all days between start_date and end_date
      while date <= end_date:
        # skip leap years
        if date.month == 2 and date.day == 29:
          date += day_inc
          continue
        # julian date is [1, 365], our arrays are [0, 364], hence -1
        julian_date = date.timetuple().tm_yday - 1
        # We want march 1st on a leap year to be the 60th date, not the 61st
        if self._is_leap_year(date) and date.month > 2:
          julian_date -= 1
        day_index = (date - first_date).days
        var_climatology[julian_date].append(self._meteor_vars[var_index][day_index])
        date += day_inc
      # average each day's values to get a 365-day climatological year
      for day_index in range(len(var_climatology)):
        var_day_mean = np.zeros(var_climatology[day_index][0].shape)
        for var_day_val in var_climatology[day_index]:
          var_day_mean += var_day_val
        var_day_mean /= len(var_climatology[day_index])
        var_climatology[day_index] = var_day_mean
      # use np arrays because they're cool
      var_climatology = np.array(var_climatology)
      # update class data structure
      self._meteor_vars[var_index] = var_climatology

  def _subset_data(self, data_list):
    subsection = self._h5_file
    for request in data_list:
      subsection = subsection[request]
    return subsection[()]

  def _find_pft_to_claimed_sites(self):
    # a site is "claimed" by a pft when that pft is the dominant pft in that region
    pft_to_claimed_sites = defaultdict(list)
    pft_grid_index = 0
    for pft_grid, in zip(self._pft_grids):
      dominant_pfts = stats.mode(pft_grid)[0]
      for dominant_pft in dominant_pfts:
        pft_to_claimed_sites[dominant_pft].append(pft_grid_index)
      pft_grid_index += 1
    return pft_to_claimed_sites
