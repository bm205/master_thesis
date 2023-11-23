import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

from master_thesis.simple_icd_10_cm import SimpleIcd10Cm
from master_thesis.simple_icd_10_pcs import SimpleIcd10Pcs
from master_thesis.drg_to_icd_cm import Drg_to_icd_cm
from master_thesis.hcpcs import Hcpcs
from master_thesis.preprocessing import Preprocesser
from master_thesis.similarity_levels import SimilarityLevels
from master_thesis.model_wrapper import ModelWrapper


if __name__ == "__main__":
    preprocesser_pcs = Preprocesser(SimpleIcd10Pcs)
    sim_lvls_pcs = SimilarityLevels(SimpleIcd10Pcs)
    print(sim_lvls_pcs.get_ic1('Section 0'))
    exit()

    preprocesser_cm = Preprocesser(SimpleIcd10Cm)
    sim_lvls_cm = SimilarityLevels(SimpleIcd10Cm)

    preprocesser_hcpcs = Preprocesser(Hcpcs)
    sim_lvls_hcpcs = SimilarityLevels(Hcpcs)

    preprocesser_drg = Preprocesser(Drg_to_icd_cm)
    sim_lvls_drg = SimilarityLevels(Drg_to_icd_cm)

    data_cm = pd.read_csv('data/diagnoses_icd.csv')
    data_pcs = pd.read_csv('data/procedures_icd.csv')
    data_drg = pd.read_csv('data/drg_to_icd.csv')
    data_hcpcs = pd.read_csv('data/hcpcsevents.csv')
    data_hcpcs = preprocesser_hcpcs.filtering_hcpcs(data_hcpcs)
    print(data_hcpcs)
    exit()
    data_service = pd.read_csv('data/services.csv')
    preprocesser_cm.filtering_services(data_service)

    join_cm = preprocesser_cm.filter_join(data_cm,data_service)
    join_pcs = preprocesser_pcs.filter_join(data_pcs,data_service)

    train_patients_raw_cm = join_cm.iloc[0:200]
    test_patients_raw_cm = join_cm.iloc[240:2000]

    train_patients_raw_pcs = join_pcs.iloc[0:200]
    test_patients_raw_pcs = join_pcs.iloc[240:2000]

    join_train = pd.merge(train_patients_raw_cm,train_patients_raw_pcs,on='hadm_id',how='inner')
    join_train = join_train[['hadm_id']].drop_duplicates(subset=['hadm_id'])
    join_train_cm = pd.merge(join_train,train_patients_raw_cm,on='hadm_id',how='inner')
    join_train_pcs = pd.merge(join_train,train_patients_raw_pcs,on='hadm_id',how='inner')

    join_test = pd.merge(test_patients_raw_cm,test_patients_raw_pcs,on='hadm_id',how='inner')
    join_test = join_test.drop_duplicates(subset=['hadm_id'])
    join_test_cm = pd.merge(join_test,test_patients_raw_cm,on='hadm_id',how='inner')
    join_test_pcs = pd.merge(join_test,test_patients_raw_pcs,on='hadm_id',how='inner')
    # print(join_train_cm)
    # print(join_train_pcs)
    
    print(join_test)
    # print(join_test_cm)
    # print(join_test_pcs)

    # train_patients_cm = preprocesser_cm.get_patients(join_train_cm)
    # train_patients_pcs = preprocesser_pcs.get_patients(join_train_pcs)

    # test_patients_cm= preprocesser_cm.get_patients(join_test_cm)
    # test_patients_pcs= preprocesser_pcs.get_patients(join_test_pcs)
    exit()

    y_train_cm = ModelWrapper.get_y(train_patients_cm)
    y_train_pcs = ModelWrapper.get_y(train_patients_pcs)

    X_train = ModelWrapper.get_distance_matrix(
        train_patients,
        sim_lvls_cm.get_ic2,
        sim_lvls_cm.get_cs4,
        sim_lvls_cm.get_ss2
        )

    X_train_dist_matrix = X_train
    X_test= ModelWrapper.get_test_distance(
        test_patients,
        train_patients,
        sim_lvls_cm.get_ic2,
        sim_lvls_cm.get_cs4,
        sim_lvls_cm.get_ss2
        )

    X_test_dist_matrix = X_test

    k = 1
    knn_classifier = KNeighborsClassifier(n_neighbors=k, metric='precomputed')
    knn_classifier.fit(X_train_dist_matrix, y_train)

    y_pred = knn_classifier.predict(X_test_dist_matrix)
    y_actual = ModelWrapper.get_y(test_patients_raw)

    cm = confusion_matrix(y_actual, y_pred)
