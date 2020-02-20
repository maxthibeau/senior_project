import h5py
class ReferenceInput():
  def __init__(self, filepath):
    self._h5_file = h5py.File(filepath, 'r')

  def subset_data(self, data_list):
    subsection = self._h5_file
    for request in data_list:
      subsection = subsection[request]
    return subsection[()]
