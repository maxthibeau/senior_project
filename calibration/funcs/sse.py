import numpy as np

# n_s is the number of non-missing cases for a tower site
def rmse(n_s, obs, pred):
  # equation 16
  return 1 / (n_s - 1) * np.sqrt(np.sum(obs - pred)**2))

def sse(all_obs, all_pred):

  # equation 17  
  for obs, pred in zip(all_obs, all_pred):
    n_s = np.nansum(all_obs)

  return 100 * 
