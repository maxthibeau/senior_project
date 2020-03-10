import pandas as pd
class SingleFluxTower():    
  def __init__(self, flux_tower_fname):
    df = pd.read_csv(flux_tower_fname)
    self._gpp = df['gpp'].to_numpy()
    self._reco = df['reco'].to_numpy()
    self._nee = df['nee'].to_numpy()
    self._tower_vars = [self._gpp, self._reco, self._nee]

  def gpp(self):
    return self._tower_vars[0]

  def reco(self):
    return self._tower_vars[1]

  def nee(self):
    return self._tower_vars[2]

  def tower_vars(self):
    return self._tower_vars
