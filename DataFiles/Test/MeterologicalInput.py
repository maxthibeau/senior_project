import sys

class MeterologicalInput():
  
  def __init__(self, h5_file):
    self._pft_grids = h5_file['ANC']['lc_dom'][()].T
    self._site_names = h5_file['SUBSET']['site_name'][()].ravel()
    self._pfts = np.unique(self._pft_grids)

  def pfts(self):
    return self._pfts          

  def pft_grids(self):
    return self._pft_grids

  def site_names(self):
    return self._site_names

def main(argv):
  if len(argv < 1):
    print "usage: <.h5 file>"
  fname = argv[0]
  h5_file = h5py.File(fname, 'r')
  meterological_input = Meterological_input(h5_file)

if __name__ == "__main__":
  main(sys.argv[1:])
