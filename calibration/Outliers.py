import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import pandas as pd

class Outliers:
    #outlier options:
    #SciPy’s filtfilt - scipy.signal.filtfilt(b, a, x, axis=-1, padtype='odd', padlen=None, method='pad', irlen=None) https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html
    #SavitzkyGolay filter - scipy.signal.savgol_filter(x, window_length, polyorder, deriv=0, delta=1.0, axis=-1, mode='interp', cval=0.0) https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.signal.savgol_filter.html
    #robust spline smoothing - scipy.interpolate.UnivariateSpline(x, y, w=None, bbox=[None, None], k=3, s=None, ext=0, check_finite=False) https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.interpolate.UnivariateSpline.html
    def __init__(self,pft,tower_fnames,reference_input,window_size):
        self.pft = pft
        self.tower_fnames = tower_fnames
        self.ref = reference_input
        self.window_size = window_size
        self.gpp_sd = 0.0
        self.gpp_mean = self.get_mean("GPP")
        self.reco_sd = 0.0
        self.reco_mean = self.get_mean("RECO")
        self.gpp_all_towers = []
        self.reco_all_towers = []

        # TODO: nans and negative vals
        for tower_fname in self.tower_fnames:
            df = pd.read_csv(tower_fname)
            gpp_single_tower = df['gpp'].to_numpy()
            reco_single_tower = df['reco'].to_numpy()

            # remove non-negative values from gpp and reco
            gpp_single_tower[gpp_single_tower < 0] = np.nan
            reco_single_tower[reco_single_tower < 0] = np.nan

            self.gpp_all_towers.append(gpp_single_tower)
            self.reco_all_towers.append(reco_single_tower)

    def get_mean(self,choice):
        if(choice == "GPP"):
            self.gpp_sd = self.ref.subset_data(["GPP","gpp_std_dev"])
            return self.ref.gpp_given_pft(self.pft)
        elif(choice == "RECO"):
            self.reco_sd = self.ref.subset_data(["RH","rh_std_dev"])
            return self.ref.reco_given_pft(self.pft)

    def display_GPP(self):
        base = np.array(list(i/100 for i in range(0,self.window_size)))
        b = np.ones(self.window_size) / self.window_size
        #smooth data
        y = signal.filtfilt(b,1,self.gpp_all_towers,method='gust')
        plt.plot(base,y,'r')
        plt.show()

    def display_RECO(self):
        base = np.array(list(i/100 for i in range(0,self.window_size)))
        b = np.ones(self.window_size) / self.window_size
        #smooth data
        y = signal.filtfilt(b,1,self.reco_all_towers,method='gust')
        plt.plot(base,y,'r')
        plt.show()

    def display_outliers(self):
        self.display_GPP()
        self.display_RECO()
