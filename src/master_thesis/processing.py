import pandas as pd
import numpy as np
import master_thesis.config as config
from master_thesis.preprocessing import Preprocesser
from master_thesis.model_wrapper import ModelWrapper
from master_thesis.similarity_levels import SimilarityLevels
from master_thesis.simple_icd_10_cm import SimpleIcd10Cm
from master_thesis.simple_icd_10_pcs import SimpleIcd10Pcs
from master_thesis.drg_to_icd_cm import Drg_to_icd_cm
from master_thesis.hcpcs import Hcpcs
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

class Processer:
    """Processing"""
    @staticmethod
    def process_4_tax():
        sim_lvls_cm = SimilarityLevels(SimpleIcd10Cm)
        preprocesser_cm = Preprocesser(SimpleIcd10Cm)
        sim_lvls_pcs = SimilarityLevels(SimpleIcd10Pcs)
        preprocesser_pcs = Preprocesser(SimpleIcd10Pcs)
        sim_lvls_drg = SimilarityLevels(Drg_to_icd_cm)
        preprocesser_drg = Preprocesser(Drg_to_icd_cm)
        sim_lvls_hcpcs = SimilarityLevels(Hcpcs)
        preprocesser_hcpcs = Preprocesser(Hcpcs)

        # data_cm = pd.read_csv('data/diagnoses_icd.csv')
        data_cm = pd.read_csv('data/draft1.csv')
        data_cm = Preprocesser.filtering_icd(data_cm)
        # data_pcs = pd.read_csv('data/procedures_icd.csv')
        data_pcs = pd.read_csv('data/draft2.csv')
        data_pcs = Preprocesser.filtering_icd(data_pcs)
        # data_drg = pd.read_csv('data/drg_to_icd.csv')
        data_drg = pd.read_csv('data/draft3.csv')
        # data_hcpcs = pd.read_csv('data/hcpcsevents.csv')
        data_hcpcs = pd.read_csv('data/draft4.csv')
        data_hcpcs = Preprocesser.filtering_hcpcs(data_hcpcs)
        # data_service = pd.read_csv('data/services.csv')
        data_service = pd.read_csv('data/draft5.csv')
        # data_service = Preprocesser.filtering_services(data_service)
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
        train_cm_patients_list = preprocesser_cm.get_patients(train_cm_patients)
        train_pcs_patients_list = preprocesser_pcs.get_patients(train_pcs_patients)
        train_drg_patients_list = preprocesser_drg.get_patients(train_drg_patients)
        train_hcpcs_patients_list = preprocesser_hcpcs.get_patients(train_hcpcs_patients)
        test_cm_patients_list = preprocesser_cm.get_patients(test_cm_patients)
        test_pcs_patients_list = preprocesser_pcs.get_patients(test_pcs_patients)
        test_drg_patients_list = preprocesser_drg.get_patients(test_drg_patients)
        test_hcpcs_patients_list = preprocesser_hcpcs.get_patients(test_hcpcs_patients)

        y_train = ModelWrapper.get_y(train_cm_patients)

        X_train_cm = ModelWrapper.get_distance_matrix(
            train_cm_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_cm),
            Preprocesser.choose_cs_metric(sim_lvls_cm),
            Preprocesser.choose_ss_metric(sim_lvls_cm)
            )
        # print(X_train_cm)
        
        X_train_pcs = ModelWrapper.get_distance_matrix(
            train_pcs_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_pcs),
            Preprocesser.choose_cs_metric(sim_lvls_pcs),
            Preprocesser.choose_ss_metric(sim_lvls_pcs)
            )
        # print(X_train_pcs)

        X_train_drg = ModelWrapper.get_distance_matrix(
            train_drg_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_drg),
            Preprocesser.choose_cs_metric(sim_lvls_drg),
            Preprocesser.choose_ss_metric(sim_lvls_drg)
            )
        # print(X_train_drg)
        
        X_train_hcpcs = ModelWrapper.get_distance_matrix(
            train_hcpcs_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_hcpcs),
            Preprocesser.choose_cs_metric(sim_lvls_hcpcs),
            Preprocesser.choose_ss_metric(sim_lvls_hcpcs)
            )
        # print(X_train_hcpcs)

        X_train_dist_matrix_cm = np.multiply(X_train_cm, config.WEIGHTS[0])
        X_train_dist_matrix_pcs = np.multiply(X_train_pcs, config.WEIGHTS[1])
        X_train_dist_matrix_drg = np.multiply(X_train_drg, config.WEIGHTS[2])
        X_train_dist_matrix_hcpcs = np.multiply(X_train_hcpcs, config.WEIGHTS[3])
        X_train_dist_matrix = np.array(X_train_dist_matrix_cm) + np.array(X_train_dist_matrix_pcs) + np.array(X_train_dist_matrix_drg) + np.array(X_train_dist_matrix_hcpcs)
        print(X_train_dist_matrix)

        X_test_cm= ModelWrapper.get_test_distance(
            test_cm_patients_list,
            train_cm_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_cm),
            Preprocesser.choose_cs_metric(sim_lvls_cm),
            Preprocesser.choose_ss_metric(sim_lvls_cm)
            )
        
        X_test_pcs= ModelWrapper.get_test_distance(
            test_pcs_patients_list,
            train_pcs_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_pcs),
            Preprocesser.choose_cs_metric(sim_lvls_pcs),
            Preprocesser.choose_ss_metric(sim_lvls_pcs)
            )
        
        X_test_drg= ModelWrapper.get_test_distance(
            test_drg_patients_list,
            train_drg_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_drg),
            Preprocesser.choose_cs_metric(sim_lvls_drg),
            Preprocesser.choose_ss_metric(sim_lvls_drg)
            )
        
        X_test_hcpcs= ModelWrapper.get_test_distance(
            test_hcpcs_patients_list,
            train_hcpcs_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_hcpcs),
            Preprocesser.choose_cs_metric(sim_lvls_hcpcs),
            Preprocesser.choose_ss_metric(sim_lvls_hcpcs)
            )

        X_test_dist_matrix_cm = np.multiply(X_test_cm, config.WEIGHTS[0])
        X_test_dist_matrix_pcs = np.multiply(X_test_pcs, config.WEIGHTS[1])
        X_test_dist_matrix_drg = np.multiply(X_test_drg, config.WEIGHTS[2])
        X_test_dist_matrix_hcpcs = np.multiply(X_test_hcpcs, config.WEIGHTS[3])
        X_test_dist_matrix = np.array(X_test_dist_matrix_cm) + np.array(X_test_dist_matrix_pcs) + np.array(X_test_dist_matrix_drg) + np.array(X_test_dist_matrix_hcpcs)
        print(X_test_dist_matrix)

        k = config.K
        knn_classifier = KNeighborsClassifier(n_neighbors=k, metric='precomputed')
        knn_classifier.fit(X_train_dist_matrix, y_train)

        y_pred = knn_classifier.predict(X_test_dist_matrix)
        y_actual = ModelWrapper.get_y(test_cm_patients)

        cm = confusion_matrix(y_actual, y_pred)

        print('=============')
        print(y_pred)
        print(y_actual)
        print(f'confusion matrix: \n{cm}')

        print(f'f1_score: {f1_score(y_actual, y_pred,average="weighted")}')

        print(f'accuracy_score: {accuracy_score(y_actual, y_pred)}')

    @staticmethod
    def process_2_tax():        
        data = []
        sim_lvls_1 = None
        sim_lvls_2 = None
        preprocesser_1 = None
        preprocesser_2 = None

        if 'cm' in config.TAXONOMIES:
            data_cm = pd.read_csv('./data/draft1.csv')
            data_cm = Preprocesser.filtering_icd(data_cm)
            sim_lvls_1 = SimilarityLevels(SimpleIcd10Cm)
            preprocesser_1 = Preprocesser(SimpleIcd10Cm)
            print('TAX = cm')
        else:
            data_cm = pd.DataFrame(data)
        if 'pcs' in config.TAXONOMIES:
            data_pcs = pd.read_csv('./data/draft2.csv')
            data_pcs = Preprocesser.filtering_icd(data_pcs)
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
            data_hcpcs = Preprocesser.filtering_hcpcs(data_hcpcs)
            sim_lvls_2 = SimilarityLevels(Hcpcs)
            preprocesser_2 = Preprocesser(Hcpcs)
            print('TAX = hcpcs')
        else:
            data_hcpcs = pd.DataFrame(data)
            
        tax_1,tax_2 = Preprocesser.get_data_2_tax(data_cm,data_pcs,data_drg,data_hcpcs)
        data_service = pd.read_csv('./data/draft5.csv')
        # data_service = Preprocesser.filtering_services(data_service)
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
        # print(X_train_1)
        
        X_train_2 = ModelWrapper.get_distance_matrix(
            train_tax_2_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls_2),
            Preprocesser.choose_cs_metric(sim_lvls_2),
            Preprocesser.choose_ss_metric(sim_lvls_2)
            )
        # print(X_train_2)

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

        k = config.K
        knn_classifier = KNeighborsClassifier(n_neighbors=k, metric='precomputed')
        knn_classifier.fit(X_train_dist_matrix, y_train)

        y_pred = knn_classifier.predict(X_test_dist_matrix)
        y_actual = ModelWrapper.get_y(test_tax_1_patients)

        cm = confusion_matrix(y_actual, y_pred)

        print('=============')
        print(y_pred)
        print(y_actual)
        print(f'confusion matrix: \n{cm}')

        print(f'f1_score: {f1_score(y_actual, y_pred,average="weighted")}')

        print(f'accuracy_score: {accuracy_score(y_actual, y_pred)}')

    @staticmethod
    def process_1_tax():

        if 'cm' in config.TAXONOMIES:
            data = pd.read_csv('./data/draft1.csv')
            data = Preprocesser.filtering_icd(data)
            sim_lvls = SimilarityLevels(SimpleIcd10Cm)
            preprocesser_tax = Preprocesser(SimpleIcd10Cm)
            print('TAX = cm')

        elif 'pcs' in config.TAXONOMIES:
            data = pd.read_csv('./data/draft2.csv')
            data = Preprocesser.filtering_icd(data)
            sim_lvls = SimilarityLevels(SimpleIcd10Pcs)
            preprocesser_tax = Preprocesser(SimpleIcd10Pcs)
            print('TAX = pcs')

        elif 'drg' in config.TAXONOMIES:
            data = pd.read_csv('./data/draft3.csv')
            sim_lvls = SimilarityLevels(Drg_to_icd_cm)
            preprocesser_tax = Preprocesser(Drg_to_icd_cm)
            print('TAX = drg')

        elif 'hcpcs' in config.TAXONOMIES:
            data = pd.read_csv('./data/draft4.csv')
            data = Preprocesser.filtering_hcpcs(data)
            sim_lvls = SimilarityLevels(Hcpcs)
            preprocesser_tax = Preprocesser(Hcpcs)
            print('TAX = hcpcs')

        data_service = pd.read_csv('./data/draft5.csv')
        # data_service = Preprocesser.filtering_services(data_service)
        data_service = data_service[['hadm_id','curr_service']]
        data_for_merge = data[['hadm_id']]
        data_for_merge = data_for_merge.drop_duplicates()
        all_patients = pd.merge(data_for_merge,data_service,on='hadm_id',how='inner')
        train_labeled_patients = np.array_split(all_patients,2)[0]
        test_labeled_patients = np.array_split(all_patients,2)[1]
        train_patients = pd.merge(train_labeled_patients,data,on='hadm_id',how='inner')
        test_patients = pd.merge(test_labeled_patients,data,on='hadm_id',how='inner')
        train_patients_list = preprocesser_tax.get_patients(train_patients)
        test_patients_list = preprocesser_tax.get_patients(test_patients)
        
        y_train = ModelWrapper.get_y(train_patients)

        X_train = ModelWrapper.get_distance_matrix(
            train_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls),
            Preprocesser.choose_cs_metric(sim_lvls),
            Preprocesser.choose_ss_metric(sim_lvls)
            )

        X_train_dist_matrix = X_train
        print(X_train_dist_matrix)

        X_test= ModelWrapper.get_test_distance(
            test_patients_list,
            train_patients_list,
            Preprocesser.choose_ic_metric(sim_lvls),
            Preprocesser.choose_cs_metric(sim_lvls),
            Preprocesser.choose_ss_metric(sim_lvls)
            )

        X_test_dist_matrix = X_test
        print(X_test_dist_matrix)

        k = config.K
        knn_classifier = KNeighborsClassifier(n_neighbors=k, metric='precomputed')
        knn_classifier.fit(X_train_dist_matrix, y_train)

        y_pred = knn_classifier.predict(X_test_dist_matrix)
        y_actual = ModelWrapper.get_y(test_patients)

        cm = confusion_matrix(y_actual, y_pred)

        print('=============')
        print(y_pred)
        print(y_actual)
        print(f'confusion matrix: \n{cm}')

        print(f'f1_score: {f1_score(y_actual, y_pred,average="weighted")}')

        print(f'accuracy_score: {accuracy_score(y_actual, y_pred)}')


    # num_of_tax = input("Enter number of taxonomies, either 1, 2, or 4:")
    # print("Username is: " + num_of_tax)

# ===================