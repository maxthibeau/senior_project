class Parameters:
  def __init__(self):
    self.old_lue_max = None
    self.old_vpd_low = None
    self.old_vpd_high = None
    self.old_smrz_low = None
    self.old_smrz_hi = None
    self.old_tmin_low = None
    self.old_tmin_hi = None
    self.old_ft = None
    
    self.new_lue_max = None
    self.new_vpd_low = None
    self.new_vpd_high = None
    self.new_smrz_low = None
    self.new_smrz_hi = None
    self.new_tmin_low = None
    self.new_tmin_hi = None
    self.new_ft = None

    self.log = ""

  def old_lue_max(self):
    return self.old_lue_max
  def old_vpd_low(self):
    return self.old_vpd_low
  def old_vpd_high(self):
    return self.old_vpd_high
  def old_smrz_low(self):
    return self.old_smrz_low
  def old_smrz_hi(self):
    return self.old_smrz_hi
  def old_tmin_low(self):
    return self.old_tmin_low
  def old_tmin_hi(self):
    return self.old_tmin_hi
  def old_ft(self):
    return self.old_ft

  def new_lue_max(self):
    return self.new_lue_max
  def new_vpd_low(self):
    return self.new_vpd_low
  def new_vpd_high(self):
    return self.new_vpd_high
  def new_smrz_low(self):
    return self.new_smrz_low
  def new_smrz_hi(self):
    return self.new_smrz_hi
  def new_tmin_low(self):
    return self.new_tmin_low
  def new_tmin_hi(self):
    return self.new_tmin_hi
  def new_ft(self):
    return self.new_ft

  def log(self):
    return self.log

#######################
# Setters
#######################

  def set_old_lue_max(self,val):
    self.old_lue_max = val
  def set_old_vpd_low(self,val):
    self.old_vpd_low = val
  def set_old_vpd_high(self,val):
    self.old_vpd_high = val
  def set_old_smrz_low(self,val):
    self.old_smrz_low = val
  def set_old_smrz_hi(self,val):
    self.old_smrz_hi = val
  def set_old_tmin_low(self,val):
    self.old_tmin_low = val
  def set_old_tmin_hi(self,val):
    self.old_tmin_hi = val
  def set_old_ft(self,val):
    self.old_ft = val

  def set_new_lue_max(self,val):
    self.new_lue_max = val
  def set_new_vpd_low(self,val):
    self.new_vpd_low = val
  def set_new_vpd_high(self,val):
    self.new_vpd_high = val
  def set_new_smrz_low(self,val):
    self.new_smrz_low = val
  def set_new_smrz_hi(self,val):
    self.new_smrz_hi = val
  def set_new_tmin_low(self,val):
    self.new_tmin_low = val
  def set_new_tmin_hi(self,val):
    self.new_tmin_hi = val
  def set_new_ft(self,val):
    self.new_ft = val

#######################
# Differs
#######################

  def get_diff_lue_max(self):
    return self.new_lue_max - self.old_lue_max
  def get_diff_vpd_low(self):
    return self.new_vpd_low - self.old_vpd_low
  def get_diff_vpd_high(self):
    return self.new_vpd_high - self.old_vpd_high
  def get_diff_smrz_low(self):
    return self.new_smrz_low - self.old_smrz_low
  def get_diff_smrz_hi(self):
    return self.new_smrz_hi - self.old_smrz_hi
  def get_diff_tmin_low(self):
    return self.new_tmin_low - self.old_tmin_low
  def get_diff_tmin_hi(self):
    return self.new_tmin_hi - self.old_tmin_hi
  def get_diff_ft(self):
    return self.new_ft - self.old_ft

######################
# Add Log
######################

  def add_log(self,text):
    self.log += text
    self.log += '\n'