import pandas as pd
import numpy as np
import master_thesis.config as config
from master_thesis.model_wrapper import ModelWrapper
from master_thesis.similarity_levels import SimilarityLevels
from master_thesis.simple_icd_10_cm import SimpleIcd10Cm
from master_thesis.simple_icd_10_pcs import SimpleIcd10Pcs
from master_thesis.drg_to_icd_cm import Drg_to_icd_cm
from master_thesis.hcpcs import Hcpcs
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import confusion_matrix

class Preprocesser:
    """Preprocessing"""
    def __init__(self, taxonomy) -> None:
        self.tax = taxonomy()

    def get_patients(self, patients_list) -> list[list[str]]:
        """get list of concepts of patients & remove patients with not a valid concept"""
        if 'icd_code' in patients_list:
            code_column = 'icd_code'
        elif 'hcpcs_cd' in patients_list:
            code_column = 'hcpcs_cd'
        patients = []
        for _, row in patients_list.iterrows():
            if row['seq_num'] == 1:
            # if row['seq_num']%4 == 0:
                patient = []
                patients.append(patient)
                print(row['hadm_id'])
                if self.tax.is_valid_item(row[code_column]) == True:
                    patient.append(row[code_column])
                else:
                    print(f"Oops!  The code {row[code_column]} is not valid in the taxonomy. It will be removed from the patient.")
            elif row['seq_num'] != 1 and patients == []:
                continue
            else: 
                if self.tax.is_valid_item(row[code_column]) == True:
                    patient.append(row[code_column])
                else:
                    print(f"Oops!  The code {row[code_column]} is not valid in the taxonomy. It will be removed from the patient.")

        # Remove empty patients
        patients = [ele for ele in patients if ele != []]
        
        patients_num = len(patients)
        print(patients_num)
        print(patients)
        return patients
    
    def filtering_icd(icd_data):
        icd10 = icd_data.loc[icd_data['icd_version'] == 10]
        icd_data = icd10[['hadm_id','seq_num','icd_code']]

        return icd_data
    
    def filtering_hcpcs(hcpcsevents):
        filtered = hcpcsevents[hcpcsevents["hcpcs_cd"].str.match('^[A-Z]')]
        previous_row = ''
        counter = 1
        for index,row in filtered.iterrows():
            if row['hadm_id'] == previous_row:
                counter = counter + 1
            else:
                counter = 1
            filtered.at[index,'seq_num']= counter
            previous_row = row['hadm_id']

        filtered.to_csv('data/hcpcs_filtered.csv')
        return filtered
    
    def filtering_services(services):
        previous_service = ''
        for index,row in services.iterrows():
            if row['prev_service'] is not np.nan:
                services['curr_service'][index] = previous_service + ' ' + services['curr_service'][index]
                if row['hadm_id'] != services['hadm_id'][index+1]:
                    services['prev_service'][index] = np.nan
                else:
                    services['prev_service'][index] = 'delete'
            else:
                if row['hadm_id'] == services['hadm_id'][index+1]:
                    services['prev_service'][index] = 'delete'
            previous_service =  services['curr_service'][index]

        filtered_services = services[services['prev_service']!='delete']
        filtered_services

        filtered_services.to_csv('../data/service_filtered.csv')
        return filtered_services
    
    def get_data_2_tax(data_tax_1,data_tax_2,data_tax_3,data_tax_4):
        data = []
        a = pd.DataFrame(data)
        b = pd.DataFrame(data)
        if not data_tax_1.empty:
            a = data_tax_1
        if not data_tax_2.empty:
            if a.empty:
                a = data_tax_2
            else:
                b = data_tax_2
        if not data_tax_3.empty:
            if a.empty:
                a = data_tax_3
            else:
                b = data_tax_3
        if not data_tax_4.empty:
            b = data_tax_4

        return a,b

    def join_data_2_tax(data_tax_1,data_tax_2,labeled_data):
        data_tax_1 = data_tax_1[['hadm_id']]
        data_tax_2 = data_tax_2[['hadm_id']]
        data_tax_1 = data_tax_1.drop_duplicates()
        data_tax_2 = data_tax_2.drop_duplicates()
        join0 = pd.merge(data_tax_1,data_tax_2,on='hadm_id',how='inner')
        join = pd.merge(labeled_data,join0,on='hadm_id',how='inner')

        return join
    
    def join_data_4_tax(data_cm,data_pcs,data_drg,data_hcpcs,labeled_data):
        data_cm = data_cm[['hadm_id']]
        data_pcs = data_pcs[['hadm_id']]
        data_drg = data_drg[['hadm_id']]
        data_hcpcs = data_hcpcs[['hadm_id']]
        data_cm = data_cm.drop_duplicates()
        data_pcs = data_pcs.drop_duplicates()
        data_drg = data_drg.drop_duplicates()
        data_hcpcs = data_hcpcs.drop_duplicates()
        join0 = pd.merge(data_cm,data_pcs,on='hadm_id',how='inner')
        join1 = pd.merge(join0,data_drg,on='hadm_id',how='inner')
        join2 = pd.merge(join1,data_hcpcs,on='hadm_id',how='inner')
        join = pd.merge(labeled_data,join2,on='hadm_id',how='inner')

        return join
    
    def choose_ic_metric(function):
        ic = None
        if config.IC == 1:
            print('IC1 is chosen!')
            ic = function.get_ic1
        elif config.IC == 2:
            print('IC2 is chosen!')
            ic = function.get_ic2
        else:
            print('Wrong number. IC1 is considered.')
            ic = function.get_ic1
        return ic

    def choose_cs_metric(function):
        cs = None
        if config.CS == 1:
            print('CS1 is chosen!')
            cs = function.get_cs1
        elif config.CS == 2:
            print('CS2 is chosen!')
            cs = function.get_cs2
        else:
            print('Wrong number. CS1 is considered.')
            cs = function.get_cs1
        return cs

    def choose_ss_metric(function):
        ss = None
        if config.SS == 1:
            print('SS1 is chosen!')
            ss = function.get_ss1
        elif config.SS == 2:
            print('SS2 is chosen!')
            ss = function.get_ss2
        elif config.SS == 3:
            print('SS3 is chosen!')
            ss = function.get_ss3
        elif config.SS == 4:
            print('SS4 is chosen!')
            ss = function.get_ss4
        else:
            print('Wrong number. SS1 is considered.')
            ss = function.get_ss1
        return ss
        
    
    def process_4_tax():
        data_cm = pd.read_csv('data/diagnoses_icd.csv')
        data_cm = Preprocesser.filtering_icd(data_cm)
        data_pcs = pd.read_csv('data/procedures_icd.csv')
        data_pcs = Preprocesser.filtering_icd(data_pcs)
        data_drg = pd.read_csv('data/drg_to_icd.csv')
        data_hcpcs = pd.read_csv('data/hcpcsevents.csv')
        data_hcpcs = Preprocesser.filtering_hcpcs(data_hcpcs)
        data_service = pd.read_csv('data/services.csv')
        data_service = Preprocesser.filtering_services(data_service)
        data_service = data_service[['hadm_id','curr_service']]
        all_patients = Preprocesser.join_data_4_tax(data_cm,data_pcs,data_drg,data_hcpcs,data_service)
        train_all_patients = np.array_split(all_patients,2)[0]
        test_all_patients = np.array_split(all_patients,2)[1]
        train_cm_patients = pd.merge(train_all_patients,data_cm,on='hadm_id',how='inner')
        test_cm_patients = pd.merge(test_all_patients,data_cm,on='hadm_id',how='inner')
        train_pcs_patients = pd.merge(train_all_patients,data_pcs,on='hadm_id',how='inner')
        test_pcs_patients = pd.merge(test_all_patients,data_pcs,on='hadm_id',how='inner')
        train_drg_patients = pd.merge(train_all_patients,data_drg,on='hadm_id',how='inner')
        test_drg_patients = pd.merge(test_all_patients,data_drg,on='hadm_id',how='inner')
        train_hcpcs_patients = pd.merge(train_all_patients,data_hcpcs,on='hadm_id',how='inner')
        test_hcpcs_patients = pd.merge(test_all_patients,data_hcpcs,on='hadm_id',how='inner')
        train_cm_patients_list = Preprocesser.get_patients(train_cm_patients)
        train_pcs_patients_list = Preprocesser.get_patients(train_pcs_patients)
        train_drg_patients_list = Preprocesser.get_patients(train_drg_patients)
        train_hcpcs_patients_list = Preprocesser.get_patients(train_hcpcs_patients)
        test_cm_patients_list = Preprocesser.get_patients(test_cm_patients)
        test_pcs_patients_list = Preprocesser.get_patients(test_pcs_patients)
        test_drg_patients_list = Preprocesser.get_patients(test_drg_patients)
        test_hcpcs_patients_list = Preprocesser.get_patients(test_hcpcs_patients)


    def process_2_tax():
        data = []
        sim_lvls_1 = None
        sim_lvls_2 = None
        preprocesser_1 = None
        preprocesser_2 = None

        if 'cm' in config.TAXONOMIES:
            data_cm = pd.read_csv('./data/draft.csv')
            sim_lvls_1 = SimilarityLevels(SimpleIcd10Cm)
            preprocesser_1 = Preprocesser(SimpleIcd10Cm)
            print('TAX = cm')
        else:
            data_cm = pd.DataFrame(data)
        if 'pcs' in config.TAXONOMIES:
            data_pcs = pd.read_csv('./data/draft2.csv')
            if sim_lvls_1 == None:
                sim_lvls_1 = SimilarityLevels(SimpleIcd10Pcs)
                preprocesser_1 = Preprocesser(SimpleIcd10Pcs)
            else:
                sim_lvls_2 = SimilarityLevels(SimpleIcd10Pcs)
                preprocesser_2 = Preprocesser(SimpleIcd10Pcs)
            print('TAX = pcs')
        else:
            data_pcs = pd.DataFrame(data)
        if 'drg' in config.TAXONOMIES:
            data_drg = pd.read_csv('./data/draft3.csv')
            if sim_lvls_1 == None:
                sim_lvls_1 = SimilarityLevels(Drg_to_icd_cm)
                preprocesser_1 = Preprocesser(Drg_to_icd_cm)
            else:
                sim_lvls_2 = SimilarityLevels(Drg_to_icd_cm)
                preprocesser_2 = Preprocesser(Drg_to_icd_cm)
            print('TAX = drg')
        else:
            data_drg = pd.DataFrame(data)
        if 'hcpcs' in config.TAXONOMIES:
            data_hcpcs = pd.read_csv('./data/draft4.csv')
            sim_lvls_2 = SimilarityLevels(Hcpcs)
            preprocesser_2 = Preprocesser(Hcpcs)
            print('TAX = hcpcs')
        else:
            data_hcpcs = pd.DataFrame(data)

        tax_1,tax_2 = Preprocesser.get_data_2_tax(data_cm,data_pcs,data_drg,data_hcpcs)
        data_service = pd.read_csv('./data/draft5.csv')
        data_service = data_service[['hadm_id','curr_service']]
        all_patients = Preprocesser.join_data_2_tax(tax_1,tax_2,data_service)
        # print(all_patients)
        train_all_patients = np.array_split(all_patients,2)[0]
        # print(train_all_patients)
        test_all_patients = np.array_split(all_patients,2)[1]
        # print(test_all_patients)
        train_tax_1_patients = pd.merge(train_all_patients,tax_1,on='hadm_id',how='inner')
        # print(train_tax_1_patients)
        test_tax_1_patients = pd.merge(test_all_patients,tax_1,on='hadm_id',how='inner')
        # print(test_tax_1_patients)
        train_tax_2_patients = pd.merge(train_all_patients,tax_2,on='hadm_id',how='inner')
        # print(train_tax_2_patients)
        test_tax_2_patients = pd.merge(test_all_patients,tax_2,on='hadm_id',how='inner')
        # print(test_tax_2_patients)
        train_tax_1_patients_list = preprocesser_1.get_patients(train_tax_1_patients)
        test_tax_1_patients_list = preprocesser_1.get_patients(test_tax_1_patients)
        train_tax_2_patients_list = preprocesser_2.get_patients(train_tax_2_patients)
        test_tax_2_patients_list = preprocesser_2.get_patients(test_tax_2_patients)
        
        y_train = ModelWrapper.get_y(train_tax_1_patients)
        # y_train_tax_2 = ModelWrapper.get_y(train_tax_2_patients)

        X_train_1 = ModelWrapper.get_distance_matrix(
            train_tax_1_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_1),
            Preprocesser.choose_cs_metric(sim_lvls_1),
            Preprocesser.choose_ss_metric(sim_lvls_1)
            )
        print(X_train_1)
        
        X_train_2 = ModelWrapper.get_distance_matrix(
            train_tax_2_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_2),
            Preprocesser.choose_cs_metric(sim_lvls_2),
            Preprocesser.choose_ss_metric(sim_lvls_2)
            )
        print(X_train_2)

        X_train_dist_matrix_1 = np.multiply(X_train_1, config.WEIGHTS[0])
        X_train_dist_matrix_2 = np.multiply(X_train_2, config.WEIGHTS[1])
        X_train_dist_matrix = np.array(X_train_dist_matrix_1) + np.array(X_train_dist_matrix_2)
        print(X_train_dist_matrix)

        X_test_1= ModelWrapper.get_test_distance(
            test_tax_1_patients_list,
            train_tax_1_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_1),
            Preprocesser.choose_cs_metric(sim_lvls_1),
            Preprocesser.choose_ss_metric(sim_lvls_1)
            )
        
        X_test_2= ModelWrapper.get_test_distance(
            test_tax_2_patients_list,
            train_tax_2_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_2),
            Preprocesser.choose_cs_metric(sim_lvls_2),
            Preprocesser.choose_ss_metric(sim_lvls_2)
            )

        X_test_dist_matrix_1 = np.multiply(X_test_1, config.WEIGHTS[0])
        X_test_dist_matrix_2 = np.multiply(X_test_2, config.WEIGHTS[1])
        X_test_dist_matrix = np.array(X_test_dist_matrix_1) + np.array(X_test_dist_matrix_2)
        print(X_test_dist_matrix)

        k = 1
        knn_classifier = KNeighborsClassifier(n_neighbors=k, metric='precomputed')
        knn_classifier.fit(X_train_dist_matrix, y_train)

        y_pred = knn_classifier.predict(X_test_dist_matrix)
        y_actual = ModelWrapper.get_y(test_patients_raw)

        cm = confusion_matrix(y_actual, y_pred)


    # num_of_tax = input("Enter number of taxonomies, either 1, 2, or 4:")
    # print("Username is: " + num_of_tax)

# ===================

    # if config.NUMRER_OF_TAXONOMIES == 4:
    #     print("TAX_1 = cm, TAX_2 = pcs, TAX_3 = drg, TAX_4 = hcpcs")
    #     print("Weights: 25%% each")
    #     process_4_tax()

    # elif config.NUMRER_OF_TAXONOMIES == 1:
    #     print('1 Taxonomy')
    # elif config.NUMRER_OF_TAXONOMIES == 2:
    #     print('2 Taxonomies')
    #     print('weights')
    #     process_2_tax()        

    # else:
    #     print("That is not a proper number. Please insert 1, 2 or 4.")