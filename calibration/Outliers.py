import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

class Outliers:
    #outlier options:
    #SciPy’s filtfilt - scipy.signal.filtfilt(b, a, x, axis=-1, padtype='odd', padlen=None, method='pad', irlen=None) https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html
    #SavitzkyGolay filter - scipy.signal.savgol_filter(x, window_length, polyorder, deriv=0, delta=1.0, axis=-1, mode='interp', cval=0.0) https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.signal.savgol_filter.html
    #robust spline smoothing - scipy.interpolate.UnivariateSpline(x, y, w=None, bbox=[None, None], k=3, s=None, ext=0, check_finite=False) https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.interpolate.UnivariateSpline.html
    def __init__(self,pft,flux_towers,reference_input,window_size):
        self.pft = pft
        self.towers = flux_towers
        self.ref = reference_input
        self.window_size = window_size
        self.gpp_sd = 0.0
        self.gpp_mean = self.get_mean("GPP")
        self.reco_sd = 0.0
        self.reco_mean = self.get_mean("RECO")
        self.gpp = []
        self.reco = []
        self.get_vals()

    def get_vals():
        for x in range(len(files)):
            flux_tower = files[x]
            flux_tower = flux_tower[:47]+'/'+flux_tower[47:]
            file = open(flux_tower)
            lines = csv.reader(row for row in file if not row.startswith('#'))
            for row in lines:
                gpp_val = row[5]
                reco_val = row[6]
                if(gpp_val != 'NaN' and gpp_val >= 0.0):
                    self.gpp.append(gpp_val)
                if(reco_val != 'NaN' and reco_val >= 0.0):
                    self.reco.append(reco_val)
            file.close()

    def get_mean(self,choice):
        pft = self.pft + 1
        if(choice == "GPP"):
            self.gpp_sd = self.ref.subset_data(["GPP","gpp_std_dev"])
            if(pft == 1):
                return self.ref.subset_data(["GPP","gpp_pft1_mean"])
            elif(pft == 2):
                return self.ref.subset_data(["GPP","gpp_pft2_mean"])
            elif(pft == 3):
                return self.ref.subset_data(["GPP","gpp_pft3_mean"])
            elif(pft == 4):
                return self.ref.subset_data(["GPP","gpp_pft4_mean"])
            elif(pft == 5):
                return self.ref.subset_data(["GPP","gpp_pft5_mean"])
            elif(pft == 6):
                return self.ref.subset_data(["GPP","gpp_pft6_mean"])
            elif(pft == 7):
                return self.ref.subset_data(["GPP","gpp_pft7_mean"])
            elif(pft == 8):
                return self.ref.subset_data(["GPP","gpp_pft8_mean"])
        elif(choice == "RECO"):
            self.reco_sd = self.ref.subset_data(["RH","rh_std_dev"])
            if(pft == 1):
                return self.ref.subset_data(["RH","rh_pft1_mean"])
            elif(pft == 2):
                return self.ref.subset_data(["RH","rh_pft2_mean"])
            elif(pft == 3):
                return self.ref.subset_data(["RH","rh_pft3_mean"])
            elif(pft == 4):
                return self.ref.subset_data(["RH","rh_pft4_mean"])
            elif(pft == 5):
                return self.ref.subset_data(["RH","rh_pft5_mean"])
            elif(pft == 6):
                return self.ref.subset_data(["RH","rh_pft6_mean"])
            elif(pft == 7):
                return self.ref.subset_data(["RH","rh_pft7_mean"])
            elif(pft == 8):
                return self.ref.subset_data(["RH","rh_pft8_mean"])
