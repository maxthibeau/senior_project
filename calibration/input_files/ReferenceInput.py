import h5py
class ReferenceInput():
  def __init__(self, filepath):
    self._h5_file = h5py.File(filepath, 'r')
    self._gpp = None
    self._reco = None

  def subset_by_pft(self, pft, tower_sites_claimed_by_pft):
    gpp_data_key = "gpp_pft" + str(pft) + "_mean"
    reco_data_key = "rh_pft" + str(pft) + "_mean"

    self._gpp = self._subset_data(["GPP", gpp_data_key])
    self._reco = self._subset_data(["RH", reco_data_key])

    self._gpp = self._gpp.take(indices = tower_sites_claimed_by_pft, axis = -1)
    self._reco = self._reco.take(indices = tower_sites_claimed_by_pft, axis = -1)    

  def gpp(self):
    if self._gpp == None:
      print("Data must be subset before accessing GPP")
    else:
      return self._gpp

  def reco(self):
    if self._reco == None:
      print("Data must be subset before accessing RECO")
    return self._reco

  def _subset_data(self, data_list):
    subsection = self._h5_file
    for request in data_list:
      subsection = subsection[request]
    return subsection[()]
