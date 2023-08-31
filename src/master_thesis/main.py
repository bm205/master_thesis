import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

from master_thesis.simple_icd_10_cm import SimpleIcd10Cm
from master_thesis.preprocessing import Preprocesser
from master_thesis.similarity_levels import SimilarityLevels
from master_thesis.model_wrapper import ModelWrapper


if __name__ == "__main__":
    preprocesser_cm = Preprocesser(SimpleIcd10Cm)
    sim_lvls_cm = SimilarityLevels(SimpleIcd10Cm)

    df1 = pd.read_csv('data/diagnoses_icd.csv')
    icd10 = df1.loc[df1['icd_version'] == 10]
    some_patients = icd10[['hadm_id','seq_num','icd_code']].head(500)

    df2 = pd.read_csv('data/services.csv')
    df2 = df2[['hadm_id','curr_service']]

    join = pd.merge(df2,some_patients,on='hadm_id',how='inner')

    train_patients_raw = join.iloc[0:12]
    test_patients_raw = join.iloc[240:254]

    train_patients = preprocesser_cm.get_patients(train_patients_raw)
    test_patients= preprocesser_cm.get_patients(test_patients_raw)
    y_train = ModelWrapper.get_y(train_patients_raw)

    X_train = ModelWrapper.get_distance_matrix(
        train_patients,
        sim_lvls_cm.get_ic2,
        sim_lvls_cm.get_cs4,
        sim_lvls_cm.get_ss6
        )

    X_train_dist_matrix = X_train
    X_test= ModelWrapper.get_test_distance(
        test_patients,
        train_patients,
        sim_lvls_cm.get_ic2,
        sim_lvls_cm.get_cs4,
        sim_lvls_cm.get_ss6
        )

    X_test_dist_matrix = X_test

    k = 1  # Replace 'k' with the number of neighbors
    knn_classifier = KNeighborsClassifier(n_neighbors=k, metric='precomputed')
    knn_classifier.fit(X_train_dist_matrix, y_train)

    y_pred = knn_classifier.predict(X_test_dist_matrix)
    y_actual = ModelWrapper.get_y(test_patients_raw)

    cm = confusion_matrix(y_actual, y_pred)
