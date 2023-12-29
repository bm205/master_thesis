import pandas as pd
import numpy as np
import master_thesis.config as config
from master_thesis.preprocessing import Preprocesser
from master_thesis.model_wrapper import ModelWrapper
from master_thesis.similarity_levels import SimilarityLevels
from master_thesis.simple_icd_10_cm import SimpleIcd10Cm
from master_thesis.simple_icd_10_pcs import SimpleIcd10Pcs
from master_thesis.drg_to_icd_cm import Drg_to_icd_cm


# if __name__ == "__main__":
#     # num_of_tax = input("Enter number of taxonomies, either 1, 2, or 4:")
#     # print("Username is: " + num_of_tax)
#     if config.NUMRER_OF_TAXONOMIES == 4:
#         print("TAX_1 = cm, TAX_2 = pcs, TAX_3 = drg, TAX_4 = hcpcs")
#         print("Weights: 0.25 each")
#         Processer.process_4_tax()

#     elif config.NUMRER_OF_TAXONOMIES == 1:
#         print('1 Taxonomy')
#         Processer.process_1_tax()

#     elif config.NUMRER_OF_TAXONOMIES == 2:
#         print('2 Taxonomies')
#         print(f'weights: {config.WEIGHTS[0]}:{config.WEIGHTS[1]}')
#         Processer.process_2_tax()

#     else:
#         print("That is not a proper number. Please insert 1, 2 or 4.")

# data_cm = pd.read_csv('data/diagnoses_icd.csv')
# # data_cm = pd.read_csv('data/draft1.csv')
# data_cm = Preprocesser.filtering_icd(data_cm)

# data_pcs = pd.read_csv('data/procedures_icd.csv')
# # data_pcs = pd.read_csv('data/draft2.csv')
# data_pcs = Preprocesser.filtering_icd(data_pcs)

# # data_drg = pd.read_csv('data/drg_to_icd.csv')
# # # data_drg = pd.read_csv('data/draft3.csv')

# data_hcpcs = pd.read_csv('data/hcpcs_filtered.csv')
# # # data_hcpcs = pd.read_csv('data/draft4.csv')
# # # data_hcpcs = Preprocesser.filtering_hcpcs(data_hcpcs)

# # data_service = pd.read_csv('data/services.csv')
# # data_service = pd.read_csv('data/draft5.csv')
# data_service = pd.read_csv('data/services_filtered.csv')
# # data_service = Preprocesser.filtering_services(data_service)
# data_service = data_service[['hadm_id','curr_service']]
# # all_patients = Preprocesser.join_data_4_tax(data_cm,data_pcs,data_drg,data_hcpcs,data_service)
# all_patients = Preprocesser.join_data_2_tax(data_pcs,data_hcpcs,data_service)

# all_patients.to_csv('data/joined_pcs_hcpcs_tax_patients.csv')

dat1 = pd.read_csv('data/pcs_hcpcs.csv')
data_service = pd.read_csv('data/services_filtered.csv')
data_service = data_service[['hadm_id','curr_service']]
join = pd.merge(dat1,data_service,on='hadm_id',how='inner')

join.to_csv('data/pcs_hcpcs_final.csv')

