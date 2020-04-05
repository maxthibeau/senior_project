import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta
from datetime import datetime
from scipy import signal
import matplotlib.pyplot as plt

class SingleFluxTower():
  def __init__(self, flux_tower_fname):
    df = pd.read_csv(flux_tower_fname)
    self._gpp = df['gpp'].to_numpy()
    self._reco = df['reco'].to_numpy()
    self._nee = df['nee'].to_numpy()
    self._tower_vars = [self._gpp, self._reco, self._nee]
    self._tower_vars_after_smoothing = []
    self._num_tower_vars = len(self._tower_vars)
    self._non_missing_observations = 0

    with np.errstate(invalid='ignore'): #nan vals in both gpp and reco will throw RuntimeWarnings
      # throw out non-physical(negative) values
      self._gpp[self._gpp < 0.0] = np.nan
      self._reco[self._reco < 0.0] = np.nan
    # we only want to calibrate using days that have all information
    self._harmonizing_mask = np.isnan(self._gpp) | np.isnan(self._reco) | np.isnan(self._nee)
    for tower_var in self._tower_vars:
      tower_var[self._harmonizing_mask] = np.nan
    self._non_missing_observations = len(self._harmonizing_mask) - np.count_nonzero(self._harmonizing_mask)

  def _is_leap_year(self, date):
    return date.year % 4 == 0

  def climatological_year(self, start_date, end_date):
    first_date = datetime(2000, 1, 1)
    assert(start_date >= first_date and end_date <= datetime.now())
    # instead of each var getting a list, we put them all in a list of lists so new flux tower vars in the future can be used
    # as of now there are 3 vars: GPP, RECO, and NEE (in that order)
    climatology_single_tower = [[] for x in range(self._num_tower_vars)]
    # define a climatologal year for each var
    for i in range(self._num_tower_vars):
      climatology_single_tower[i] = [[] for x in range(365)]
    date = start_date
    day_inc = timedelta(days=1)
    # loop through all possible dyas
    while date <= end_date:
      # handle leap years
      if date.month == 2 and date.day == 29:
        date += day_inc
        continue
      # julian date is [1, 365] our arrays are [0, 364], hence -1
      julian_date = date.timetuple().tm_yday - 1
      # We want march 1st on a leap year to be the 60th date, not the 61st
      if self._is_leap_year(date) and date.month > 2:
        julian_date -= 1
      # get index in array that corresponds to date
      date_index = (date - first_date).days
      # update climatology vars (write new lines here for new variables)
      climatology_single_tower[0][julian_date].append(self._gpp[date_index])
      climatology_single_tower[1][julian_date].append(self._reco[date_index])
      climatology_single_tower[2][julian_date].append(self._nee[date_index])
      date+= day_inc
    climatology_single_tower = np.array(climatology_single_tower)
    # NOTE: geting a mean of empty slice warning here
    # average all days together
    climatology_single_tower = np.nanmean(climatology_single_tower, axis=-1)
    return climatology_single_tower

  def smooth_gpp_outliers(self, met, window):
    self._gpp_before_smoothing = np.copy(self._gpp)
    self._smooth_outliers_single_var(self._gpp, met, window)
    self._gpp_after_smoothing = self._gpp

  def smooth_reco_outliers(self, met, window):
    self._reco_before_smoothing = np.copy(self._reco)
    self._smooth_outliers_single_var(self._reco, met, window)
    self._reco_after_smoothing = self._reco

  def _smooth_outliers_single_var(self, var, met, window):
    satisfied_with_smoothing = True
    var_no_nans = var[~self._harmonizing_mask]
    b = np.ones(window) / window
    #can this be done?
    if not var_no_nans.all():
        smoothed_var = signal.filtfilt(b, 1, var_no_nans, method = met)
        var[~self._harmonizing_mask] = smoothed_var
    #else:
        #print("empty var no nans")

  def display_gpp_smoothing(self):
    x = np.linspace(0, len(self._gpp_before_smoothing), len(self._gpp_before_smoothing))
    plt.plot(x, self._gpp_before_smoothing)
    plt.plot(x, self._gpp_after_smoothing)
    plt.title("GPP Outliers Smoothed")
    plt.show()

  def display_reco_smoothing(self):
    x = np.linspace(0, len(self._reco_before_smoothing), len(self._reco_before_smoothing))
    plt.plot(x, self._reco_before_smoothing)
    plt.plot(x, self._reco_after_smoothing)
    plt.title("RECO Outliers Smoothed")
    plt.show()

  def gpp(self):
    return self._tower_vars[0]

  def reco(self):
    return self._tower_vars[1]

  def nee(self):
    return self._tower_vars[2]

  def non_missing_observations(self):
    return self._non_missing_observations

  def tower_vars(self):
    return self._tower_vars
