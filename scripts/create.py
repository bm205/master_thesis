import pandas as pd
from master_thesis.preprocessing import Preprocesser
from master_thesis.drg_to_icd_cm import Drg_to_icd_cm
from master_thesis.similarity_levels import SimilarityLevels
from master_thesis.simple_icd_10_cm import SimpleIcd10Cm
from master_thesis.hcpcs import Hcpcs

# preprocesser_cm = Preprocesser(SimpleIcd10Cm)
# sim_lvls_cm = SimilarityLevels(SimpleIcd10Cm)

# preprocesser_hcpcs = Preprocesser(Hcpcs)
# sim_lvls_hcpcs = SimilarityLevels(Hcpcs)

# preprocesser_drg = Preprocesser(Drg_to_icd_cm)
sim_lvls_drg = SimilarityLevels(Drg_to_icd_cm)

patients1 = pd.read_csv('data/draft.csv')
# patients2 = pd.read_csv('data/draft2.csv')

# patients1_hcpcs = preprocesser_hcpcs.get_patients(patients1)
# patients2_hcpcs = preprocesser_hcpcs.get_patients(patients2)

# p1 = ['A01', 'G20']
# p2 = ['B40', 'D20']

# print(sim_lvls_drg.get_ancestors('G20'))

# print(sim_lvls_drg.get_ss6(p1, p2, sim_lvls_drg.get_ic2, sim_lvls_drg.get_cs4))
exit()
# ===============

# data = {'hadm_id': [], 'icd_code':[],'seq_num':[]}

# df = pd.DataFrame(data)

# hadm_id = ['Delhi', 'Bangalore', 'Chennai', 'Patna']
# icd_code = ['G0378', 'G0121', 'G60t', 'C9600']
# seq_num = ['1', '2', '1', '1']
# df['hadm_id'] = hadm_id
# df['icd_code'] = icd_code
# df['seq_num'] = seq_num

# patients0 = df.to_csv('data/draft.csv')
# patients = pd.read_csv('data/draft.csv')

# # print(df)
# # data_drg = pd.read_csv('data/drg_to_icd.csv')
# # data_cm = pd.read_csv('data/diagnoses_icd.csv')
# # data_cm = data_cm.loc[data_cm['icd_version'] == 10]
# # some_patients_drg = data_drg.iloc[0:20]

# patients_hcpcs = preprocesser_hcpcs.get_patients(patients)

# # patients_drg

# # print(some_patients_drg)

# print(sim_lvls_drg.get_ancestors('G20'))
