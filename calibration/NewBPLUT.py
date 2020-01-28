#This class is for construction of the BPLUT table
import csv

class NewBPLUT():
    # base BPLUT has 44 columns,8 rows (each row specific for pft)
    # columns of BPLUT:
    # General: LC_index,LC_Label,model_code,NDVItoFPAR_scale,NDVItoFPAR_offset,
    # GPP: LUEmax, Tmin_min_K, Tmin_max_K,VPD_min_Pa, VPD_max_Pa,SMrz_min,SMrz_max,FT_min,FT_max,
    # RECO: SMtop_min,SMtop_max,Tsoil_beta0,Tsoil_beta1,Tsoil_beta2, fraut, fmet, fstr, kopt, kstr, kslw,
    # SOC/Fit Stats: Nee_QA_Rank_min,Nee_QA_Rank_max,Nee_QA_Error_min,Nee_QA_Error_max,Fpar_QA_Rank_min,Fpar_QA_Rank_max,Fpar_QA_Error_min,
    #       Fpar_QA_Error_max,FtMethod_QA_mult,FtAge_QA_Rank_min,FtAge_QA_Rank_max,FtAge_QA_Error_min,FtAge_QA_Error_max,
    #       Par_QA_Error,Tmin_QA_Error,Vpd_QA_Error,Smrz_QA_Error,Tsoil_QA_Error,Smtop_QA_Error
    def __init__(self,filepath):
        self.filepath = filepath
        self.current_bplut = []

    #loading of BPLUT from the config file
    def load_current():
        file = open(self.filepath)
        lines = csv.DictReader(csv.DictReader(row for row in file if not row.startswith('#')))
        for row in lines:
            print(row)
            self.current_bplut.append([])
            for col in row:
                self.current_bplut[row].append(row+col)
        #TODO
        file.close()
        print(self.current_bplut)
        return self.current_bplut

    #to be done after each optimization (GPP/RECO/SOC) step
    def after_optimization(ref_bplut, index_PFT, variables_optimized):
        bplut = ref_bplut
        #TODO
        return bplut
