import numpy as np

# n_s is the number of non-missing cases for a tower site
def rmse(n_s, obs, pred):
  # equation 16
  # print("N_S", n_s, n_s.shape)
  # print("obs", obs, obs.shape)
  # print("pred", pred, pred.shape)
  # print( 1.0 / (n_s - 1) * np.sqrt(np.sum((obs - pred)**2)))
  return 1.0 / ( (n_s - 1) * np.sqrt(np.nansum((obs-pred)**2, axis=0)) )

def sse(all_obs, all_pred, non_missing_obs, weights):
  return 100 * np.sum(non_missing_obs * weights * rmse(non_missing_obs, all_obs, all_pred)/np.sum(non_missing_obs))
