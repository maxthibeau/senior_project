#This class is for construction of the BPLUT table
import csv

class NewBPLUT():
    # base BPLUT has 44 columns,8 rows (each row specific for pft)
    # columns of BPLUT:
    # General: 0=LC_index,1=LC_Label,2=model_code,3=NDVItoFPAR_scale,4=NDVItoFPAR_offset,
    # GPP: 5=LUEmax, 6=Tmin_min_K, 7=Tmin_max_K, 8=VPD_min_Pa, 9=VPD_max_Pa, 10=SMrz_min, 11=SMrz_max, 12=FT_min, 13=FT_max,
    # RECO: 14=SMtop_min, 15=SMtop_max, 16=Tsoil_beta0, 17=Tsoil_beta1, 18=Tsoil_beta2, 19=fraut, 20=fmet, 21=fstr, 22=kopt, 23=kstr, 24=kslw,
    # SOC/Fit Stats: 25=Nee_QA_Rank_min, 26=Nee_QA_Rank_max, 27=Nee_QA_Error_min, 28=Nee_QA_Error_max, 29=Fpar_QA_Rank_min, 30=Fpar_QA_Rank_max, 31=Fpar_QA_Error_min,
    #       32=Fpar_QA_Error_max, 33=FtMethod_QA_mult, 34=FtAge_QA_Rank_min, 35=FtAge_QA_Rank_max, 36=FtAge_QA_Error_min, 37=FtAge_QA_Error_max,
    #       38=Par_QA_Error, 39=Tmin_QA_Error, 40=Vpd_QA_Error, 41=Smrz_QA_Error, 42=Tsoil_QA_Error, 43=Smtop_QA_Error
    def __init__(self,filepath):
        self.filepath = filepath
        self.current_bplut = []

    #loading of BPLUT from the config file
    def load_current(self):
        file = open(self.filepath)
        lines = csv.reader(row for row in file if not row.startswith('#'))
        row_count = -1
        for row in lines:
            self.current_bplut.append(row)
        #TODO
        file.close()
        print("***BPLUT TABLE***")
        print(self.current_bplut)
        return self.current_bplut

    #to be done after each optimization (GPP/RECO/SOC) step
    def after_optimization(self, index_PFT, variables_optimized):
        bplut = self.current_bplut
        print(bplut)
        #TODO
        return bplut
