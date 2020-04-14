#This class is for construction of the BPLUT table
import csv
import matplotlib.pyplot as plt

class NewBPLUT():
    # base BPLUT has 44 columns,8 rows (each row specific for pft)
    # columns of BPLUT:
    # General: 0=LC_index,1=LC_Label,2=model_code,3=NDVItoFPAR_scale,4=NDVItoFPAR_offset,
    # GPP: 5=LUEmax, 6=Tmin_min_K, 7=Tmin_max_K, 8=VPD_min_Pa, 9=VPD_max_Pa, 10=SMrz_min,
    #      11=SMrz_max, 12=FT_min, 13=FT_max,
    # RECO: 14=SMtop_min, 15=SMtop_max, 16=Tsoil_beta0, 17=Tsoil_beta1, 18=Tsoil_beta2,
    #       19=fraut, 20=fmet, 21=fstr, 22=kopt, 23=kstr, 24=kslw,
    # SOC/Fit Stats: 25=Nee_QA_Rank_min, 26=Nee_QA_Rank_max, 27=Nee_QA_Error_min,
    #       28=Nee_QA_Error_max, 29=Fpar_QA_Rank_min, 30=Fpar_QA_Rank_max, 31=Fpar_QA_Error_min,
    #       32=Fpar_QA_Error_max, 33=FtMethod_QA_mult, 34=FtAge_QA_Rank_min, 35=FtAge_QA_Rank_max,
    #       36=FtAge_QA_Error_min, 37=FtAge_QA_Error_max, 38=Par_QA_Error, 39=Tmin_QA_Error,
    #       40=Vpd_QA_Error, 41=Smrz_QA_Error, 42=Tsoil_QA_Error, 43=Smtop_QA_Error

    def __init__(self,filepath):
      file = open(filepath)
      lines = csv.reader(row for row in file if not row.startswith('#'))
      # grabs labels from first row
      self._labels = next(lines)
      # strip whitespace
      self._labels = [label.strip() for label in self._labels]
      self._current_bplut = []
      for row in lines:
          self._current_bplut.append(row)
      file.close()

      self._bplut_labels = ["LC_index","LC_Label","model_code","NDVItoFPAR_scale","NDVItoFPAR_offset",
      "LUEmax", "Tmin_min_K", "Tmin_max_K", "VPD_min_Pa", "VPD_max_Pa","SMrz_min","SMrz_max","FT_min",
      "FT_max","SMtop_min","SMtop_max","Tsoil_beta0","Tsoil_beta1","Tsoil_beta2", "fraut", "fmet",
      "fstr", "kopt", "kstr", "kslw","Nee_QA_Rank_min","Nee_QA_Rank_max","Nee_QA_Error_min",
      "Nee_QA_Error_max","Fpar_QA_Rank_min","Fpar_QA_Rank_max","Fpar_QA_Error_min","Fpar_QA_Error_max",
      "FtMethod_QA_mult","FtAge_QA_Rank_min","FtAge_QA_Rank_max","FtAge_QA_Error_min",
      "FtAge_QA_Error_max","Par_QA_Error","Tmin_QA_Error","Vpd_QA_Error","Smrz_QA_Error",
      "Tsoil_QA_Error","Smtop_QA_Error"]

      self._gpp_labels = ["LUEmax", "Tmin_min_K", "Tmin_max_K", "VPD_min_Pa", "VPD_max_Pa","SMrz_min","SMrz_max","FT_min",
      "FT_max"]
      self._reco_labels = ["SMtop_min","SMtop_max","Tsoil_beta0","Tsoil_beta1","Tsoil_beta2", "fraut"]


    def gpp_params(self, pft):
      param_vect = []
      param_vect.append(float(self[pft, 'LUEmax']))
      param_vect.append(float(self[pft, 'Tmin_min_K'])) #in K
      param_vect.append(float(self[pft, 'Tmin_max_K']))
      param_vect.append(float(self[pft, 'VPD_min_Pa'])) #in Pa
      param_vect.append(float(self[pft, 'VPD_max_Pa']))
      param_vect.append(float(self[pft, 'SMrz_min']))
      param_vect.append(float(self[pft, 'SMrz_max']))
      param_vect.append(float(self[pft, 'FT_min']))
      param_vect.append(float(self[pft, 'FT_max']))
      return param_vect

    def reco_params(self, pft):
      param_vect = []
      param_vect.append(float(self[pft, 'SMtop_min']))
      param_vect.append(float(self[pft, 'SMtop_max']))
      param_vect.append(float(self[pft, 'Tsoil_beta0']) + float(self[pft, 'Tsoil_beta1']) + float(self[pft, 'Tsoil_beta2'])/3.0)
      param_vect.append(float(self[pft, 'fraut']))
      return param_vect

    def kmult_params(self, pft):
      param_vect = []
      param_vect.append(float(self[pft, 'Tsoil_beta0']) + float(self[pft, 'Tsoil_beta1']) + float(self[pft, 'Tsoil_beta2'])/3.0)
      # hyperparams for arrhenius curve
      param_vect.append(float(self[pft, 'SMtop_min']))
      param_vect.append(float(self[pft, 'SMtop_max']))
      return param_vect

    def __getitem__(self, pft_and_key):
      pft, key = pft_and_key
      key_index = self._labels.index(key)
      return float(self._current_bplut[pft][key_index])

    def __setitem__(self, pft_and_key, value):
      pft,key = pft_and_key
      key_index = self._labels.index(key)
      self._current_bplut[pft][key_index] = float(value)

    #display differences for optimized parameter
    def display_difference(self,old,new,param):
        oldR = round(old,2)
        newR = round(new,2)
        plt.scatter(["Original"], oldR, label= "Original = "+str(oldR))
        plt.scatter(["Updated Fit"], newR, label= "Updated Fit = "+str(newR))
        plt.title(param + " Difference")
        if(oldR == newR):
            plt.xlabel("No Change during Optimization")
        plt.ylabel(param)
        #plt.set_ylim((-.1, 1.1))
        #plt.plot((1, 0), (0, 0), color='orange', ls='dashed')
        #plt.plot((0, 1), (1, 1), color='orange', ls='dashed')
        plt.legend()
        plt.show()

    #to be done after each optimization (GPP/RECO) steps
    def after_optimization(self, gpp_or_reco, pft, vars_optimized):
        #print("PFT = ",pft)
        if(gpp_or_reco == "GPP"):
            print("BPLUT GPP Parameters")
            g = 0
            for val in vars_optimized:
                label = self._gpp_labels[g]
                print("Current",label,": ",self[pft,label])
                old_val = self[pft,label]
                self[pft,label] = val #updates cell in BPLUT
                if(round(old_val,5) == round(val,5)):
                    print("New Value: ",val," (No Difference)")
                else:
                    print("New Value: ",val)
                #self.display_difference(old_val,val,label)
                g+=1
        else: #gpp_or_reco == "RECO"
            print("BPLUT RECO Parameters")
            r = 0
            for val in vars_optimized:
                label = self._reco_labels[r]
                print("Current",label,": ",self[pft,label])
                old_val = self[pft,label]
                if(round(old_val,5) == round(val,5)):
                    print("New Value: ",val," (No Difference)")
                else:
                    print("New Value: ",val)
                if(r==2):
                  avg = val/3
                  self[pft,self._reco_labels[2]] = avg #updates Tsoil in BPLUT
                  self[pft,self._reco_labels[3]] = avg
                  self[pft,self._reco_labels[4]] = avg
                  #self.display_difference(old_val,val,"Tsoil")
                  r = 5
                else:
                  self[pft,label] = val  #updates cell in BPLUT
                  #self.display_difference(old_val,val,label)
                  r+=1
