import numpy as np

def ramp_func(x, x_min_max_tup):
  x_min, x_max = x_min_max_tup
  x = x.astype(float)
  # Equation 7
  f1 = lambda x : 0
  f2 = lambda x : (x - x_min)/(x_max - x_min)
  f3 = lambda x : 1
  choicelist = [f1, f2, f3]
  condlist = [x <= x_min, (x > x_min)*(x < x_max), x >= x_max]
  return np.piecewise(x, condlist, choicelist)
