import master_thesis.config as config
from master_thesis.preprocessing import Preprocesser
from master_thesis.model_wrapper import ModelWrapper
from master_thesis.similarity_levels import SimilarityLevels
from master_thesis.simple_icd_10_cm import SimpleIcd10Cm
from master_thesis.simple_icd_10_pcs import SimpleIcd10Pcs
from master_thesis.drg_to_icd_cm import Drg_to_icd_cm
from master_thesis.hcpcs import Hcpcs


if __name__ == "__main__":
    if config.NUMRER_OF_TAXONOMIES == 4:
        print("TAX_1 = cm, TAX_2 = pcs, TAX_3 = drg, TAX_4 = hcpcs")
        print("Weights: 25%% each")
        Preprocesser.process_4_tax()

    elif config.NUMRER_OF_TAXONOMIES == 1:
        print('1 Taxonomy')
    elif config.NUMRER_OF_TAXONOMIES == 2:
        print('2 Taxonomies')
        print(f'weights: {config.WEIGHTS[0]}:{config.WEIGHTS[1]}')
        Preprocesser.process_2_tax()

    else:
        print("That is not a proper number. Please insert 1, 2 or 4.")
    
exit()

# sim_lvls_1 = SimilarityLevels(SimpleIcd10Pcs)
# preprocesser_1 = Preprocesser(SimpleIcd10Pcs)

# train_tax_1_patients_list = [['0TTB4ZZ', '07BC4ZX', '0UT9FZZ'], ['0UT2FZZ']]

# # print(sim_lvls_1.get_cs1('0TTB4ZZ','07BC4ZX',sim_lvls_1.get_ic2))
# # print(sim_lvls_1.get_ic2('Section 0'))
# # print(sim_lvls_1.get_num_of_leaves('Section 0'))

# X_train_1 = ModelWrapper.get_distance_matrix(
#     train_tax_1_patients_list,
#     sim_lvls_1.get_ic2,
#     sim_lvls_1.get_cs2,
#     sim_lvls_1.get_ss2
#     )
# print(X_train_1)