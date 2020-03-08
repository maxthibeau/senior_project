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
    def __init__(self,pft,tower_fnames,reference_input):
        self.pft = pft
        self.tower_fnames = tower_fnames
        self.ref = reference_input
        self.window_size = self.choose_window_size()
        self.gpp_sd = 0.0
        #self.gpp_mean = self.get_mean("GPP")
        self.reco_sd = 0.0
        #self.reco_mean = self.get_mean("RECO")
        self.gpp_all_towers = []
        self.reco_all_towers = []

        # TODO: nans and negative vals
        for tower_fname in self.tower_fnames:
            df = pd.read_csv(tower_fname)
            gpp_single_tower = df['gpp'].to_numpy()
            reco_single_tower = df['reco'].to_numpy()

            # remove non-negative values from gpp and reco
            with np.errstate(invalid='ignore'): #nan vals in both gpp and reco will throw RuntimeWarnings
                gpp_single_tower[gpp_single_tower < 0.0] = np.nan
                reco_single_tower[reco_single_tower < 0.0] = np.nan
            gpp_single_tower = gpp_single_tower[~np.isnan(gpp_single_tower)]
            #average GPP readings for the single flux tower
            gpp_total_tower = 0
            for g in range(len(gpp_single_tower)):
                gpp_total_tower += gpp_single_tower[g]
            gpp_for_tower = gpp_total_tower / float(len(gpp_single_tower))
            reco_single_tower = reco_single_tower[~np.isnan(reco_single_tower)]
            #average RECO readings for the single flux tower
            reco_total_tower = 0
            for r in range(len(reco_single_tower)):
                reco_total_tower += reco_single_tower[r]
            reco_for_tower = reco_total_tower / float(len(reco_single_tower))
            self.gpp_all_towers.append(gpp_for_tower)
            self.reco_all_towers.append(reco_for_tower)

    def choose_window_size(self):
        print("Choose the number of days you wish to view as your window")
        window_size = int(input("Window Size (whole number): "))
        while not isinstance(window_size,int):
          print ("That's not a valid window size")
          window_size = input("Window Size (whole number):")
        return window_size

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
        #plot GPP outliers
        #plt.plot(base,y,'r')
        #plt.show()

    def display_RECO(self):
        base = np.array(list(i/100 for i in range(0,self.window_size)))
        b = np.ones(self.window_size) / self.window_size
        #smooth data
        y = signal.filtfilt(b,1,self.reco_all_towers,method='gust')
        #plot RECO outliers
        #plt.plot(base,y,'r')
        #plt.show()

    def display_outliers(self):
        self.display_GPP()
        self.display_RECO()
