import numpy as np
import matplotlib.pyplot as plt

def upward_ramp_func(x, x_min_max_tup):
  x_min, x_max = x_min_max_tup
  x = x.astype(float)
  f1 = lambda x : 0
  f2 = lambda x : (x - x_min)/(x_max - x_min)
  f3 = lambda x : 1
  choicelist = [f1, f2, f3]
  condlist = [x <= x_min, (x > x_min)*(x < x_max), x >= x_max]
  return np.piecewise(x, condlist, choicelist)

def downward_ramp_func(x, x_min_max_tup):
  x_min, x_max = x_min_max_tup
  x = x.astype(float)
  f1 = lambda x : 1
  f2 = lambda x : 1 - (x - x_min)/(x_max - x_min)
  f3 = lambda x : 0
  choicelist = [f1, f2, f3]
  condlist = [x <= x_min, (x > x_min)*(x < x_max), x >= x_max]
  return np.piecewise(x, condlist, choicelist)

def kmult_arrhenius_curve(x, bt_soil):
  return arrhenius_curve(x, bt_soil, 66.02, 227.13)

def arrhenius_curve(x, mult, a, b):
  return np.exp( mult * ( (1 / a) - (1 / ( x - b) ) ) )

def display_ramp(x_var, y_var, ramp_func, ramp_func_params, lue, x_label, y_label):
  var_linspace = np.linspace(np.min(x_var), np.max(x_var), x_var.size)
  var_ramp_func = ramp_func(var_linspace, ramp_func_params) * lue
  #print(np.unique(var_ramp_func))
  plt.scatter(x_var, y_var, label = y_label + " vs. " + x_label)
  plt.plot(var_linspace, var_ramp_func, 'orange', label = x_label + " ramp function")
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.title(x_label + " Ramp Function")
  plt.legend()
  plt.show()
