import pandas as pd
import numpy as np
import master_thesis.config as config
from master_thesis.preprocessing import Preprocesser
from master_thesis.model_wrapper import ModelWrapper
from master_thesis.similarity_levels import SimilarityLevels
from master_thesis.simple_icd_10_cm import SimpleIcd10Cm
from master_thesis.simple_icd_10_pcs import SimpleIcd10Pcs
from master_thesis.drg_to_icd_cm import Drg_to_icd_cm
import master_thesis.train_dis_mat as tr


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

# dat1 = pd.read_csv('data/pcs_hcpcs.csv')
# data_service = pd.read_csv('data/services_filtered.csv')
# data_service = data_service[['hadm_id','curr_service']]
# join = pd.merge(dat1,data_service,on='hadm_id',how='inner')

# join.to_csv('data/pcs_hcpcs_final.csv')

# --------------------

file_path = 'data/final.csv'
data = pd.read_csv(file_path)
column_1 = data['hadm_id'][0:50]
column_2 = data['curr_service'][0:50]

for weights in config.WEIGHTS:
    X_train_cm = tr.X_train_dist_matrix_cm_4
    X_train_pcs = tr.X_train_dist_matrix_pcs_4
    X_train_drg = tr.X_train_dist_matrix_drg_4

    X_train_dist_matrix_1 = np.multiply(X_train_cm, weights[0])
    X_train_dist_matrix_2 = np.multiply(X_train_pcs, weights[1])
    X_train_dist_matrix_3 = np.multiply(X_train_drg, weights[2])
    X_train_dist_matrix = np.array(X_train_dist_matrix_1) + np.array(X_train_dist_matrix_2) + np.array(X_train_dist_matrix_3)

    df = pd.DataFrame(X_train_dist_matrix)

    # Add new columns
    ss = pd.concat([column_1,column_2,df], axis=1)
    # ss = pd.concat([column_2], axis=1)
    # df = pd.concat([df, column_2], axis=1)
    # df['hadm_id'] = 'Value1'
    # df['curr_service'] = 'Value2'

    ss.to_csv(f'X_train_dist_matrix_{weights}.csv', index=True)
