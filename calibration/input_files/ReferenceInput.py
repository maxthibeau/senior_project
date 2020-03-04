import h5py
class ReferenceInput():
  def __init__(self, filepath):
    self._h5_file = h5py.File(filepath, 'r')
    self._pft_to_gpp_keys = [["GPP","gpp_pft1_mean"],["GPP","gpp_pft2_mean"],["GPP","gpp_pft3_mean"],["GPP","gpp_pft4_mean"],["GPP","gpp_pft5_mean"],["GPP","gpp_pft6_mean"],["GPP","gpp_pft7_mean"],["GPP","gpp_pft8_mean"],["GPP","gpp_std_dev"]]
    self._pft_to_reco_keys = [["RH","rh_pft1_mean"],["RH","rh_pft2_mean"],["RH","rh_pft3_mean"],["RH","rh_pft4_mean"],["RH","rh_pft5_mean"],["RH","rh_pft6_mean"],["RH","rh_pft7_mean"],["RH","rh_pft8_mean"],["RH","rh_std_dev"]]

  def gpp_given_pft(self, pft):
    return self.subset_data(self._pft_to_gpp_key[pft])

  def reco_given_pft(self, pft):
    return self.subset_data(self._pft_to_reco_key[pft])

  def subset_data(self, data_list):
    subsection = self._h5_file
    for request in data_list:
      subsection = subsection[request]
    return subsection[()]
