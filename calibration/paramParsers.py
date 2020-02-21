


#Class for converting string to parameter list
class Params_To_Optimize:
  def __init__(self,text):
    self.lue_max = "LUEmax" in text
    self.vpd_low = "VPDlow" in text
    self.vpd_high = "VPDhigh" in text
    self.smrz_low = "SMRZlow" in text
    self.smrz_hi = "SMRZhigh" in text
    self.tmin_low = "TMINlow" in text
    self.tmin_hi = "TMINhigh" in text
    self.ft = "FT" in text

  def lue_max(self):
    return self.lue_max

  def vpd_low(self):
    return self.vpd_low

  def vpd_high(self):
    return self.vpd_high

  def smrz_low(self):
    return self.smrz_low

  def smrz_hi(self):
    return self.smrz_hi

  def tmin_low(self):
    return self.tmin_low

  def tmin_hi(self):
    return self.tmin_hi

  def ft(self):
    return self.ft

  def toggle_lue_max(self):
    self.lue_max = not self.lue_max

  def toggle_vpd_low(self):
    self.vpd_low = not self.vpd_low

  def toggle_vpd_high(self):
    self.vpd_high = not self.vpd_high

  def toggle_smrz_low(self):
    self.smrz_low = not self.smrz_low

  def toggle_smrz_hi(self):
    self.smrz_hi = not self.smrz_hi

  def toggle_tmin_low(self):
    self.tmin_low = not self.tmin_low

  def toggle_tmin_hi(self):
    self.tmin_hi = not self.tmin_hi

  def toggle_ft(self):
    self.ft = not self.ft
