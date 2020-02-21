


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
