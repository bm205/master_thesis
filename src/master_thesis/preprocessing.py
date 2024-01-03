import pandas as pd
import numpy as np
import master_thesis.config as config
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import make_scorer, f1_score

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
        if 'icd_version' in icd_data:
            icd10 = icd_data.loc[icd_data['icd_version'] == 10]
            icd_data = icd10[['hadm_id','seq_num','icd_code']]
            icd_data = icd_data.reset_index()

            return icd_data
        else:
            icd_data = icd_data[['hadm_id','seq_num','icd_code']]
            icd_data = icd_data.reset_index()
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
        # services['subject_id'] = services['subject_id'].astype(str)
        # services['hadm_id'] = services['hadm_id'].astype(str)

        grouped = services.groupby('hadm_id')
        rows_to_remove = []
        for name, group in grouped:
            if len(group) > 1:
                combined_service = ' '.join(group['curr_service'].astype(str))
                first_index = group.index[0]
                services.at[first_index, 'curr_service'] = combined_service
                rows_to_remove.extend(group.index[1:])

        services.drop(rows_to_remove, inplace=True)

        services.to_csv('data/service_filtered.csv')

        return services
    
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
    
    def get_data_3_tax(data_tax_1,data_tax_2,data_tax_3,data_tax_4):
        data = []
        a = pd.DataFrame(data)
        b = pd.DataFrame(data)
        c = pd.DataFrame(data)
        if data_tax_1.empty:
            a = data_tax_2
            b = data_tax_3
            c = data_tax_4
        elif data_tax_2.empty:
            a = data_tax_1
            b = data_tax_3
            c = data_tax_4
        elif data_tax_3.empty:
            a = data_tax_1
            b = data_tax_2
            c = data_tax_4
        elif data_tax_4.empty:
            a = data_tax_1
            b = data_tax_2
            c = data_tax_3

        return a,b,c

    def remove_patients_with_many_codes(patients):
        data = {'hadm_id': [], 'seq_num':[]}
        df = pd.DataFrame(data)

        df_ind = 0
        last_ind = len(patients)-1
        for index,row in patients.iterrows():
            if index==0:
                continue
            if index == last_ind and patients['seq_num'][index] <6:
                df.loc[df_ind] = [patients['hadm_id'][index],patients['seq_num'][index]]
            
            if patients['hadm_id'][index] != patients['hadm_id'][index-1] and patients['seq_num'][index-1] <6:
                df.loc[df_ind] = [patients['hadm_id'][index-1],patients['seq_num'][index-1]]
                df_ind = df_ind + 1
        return df

    def join_data_2_tax(data_tax_1,data_tax_2,labeled_data):
        data_tax_1_after_remove = Preprocesser.remove_patients_with_many_codes(data_tax_1)
        data_tax_2_after_remove = Preprocesser.remove_patients_with_many_codes(data_tax_2)
        data_tax_1_after_remove = data_tax_1_after_remove[['hadm_id']]
        data_tax_2_after_remove = data_tax_2_after_remove[['hadm_id']]
        join0 = pd.merge(data_tax_1_after_remove,data_tax_2_after_remove,on='hadm_id',how='inner')
        join = pd.merge(labeled_data,join0,on='hadm_id',how='inner')

        return join

    def join_data_3_tax(data_tax_1,data_tax_2,data_tax_3,labeled_data):
        data_tax_1_after_remove = Preprocesser.remove_patients_with_many_codes(data_tax_1)
        data_tax_2_after_remove = Preprocesser.remove_patients_with_many_codes(data_tax_2)
        data_tax_3_after_remove = Preprocesser.remove_patients_with_many_codes(data_tax_3)
        data_tax_1_after_remove = data_tax_1_after_remove[['hadm_id']]
        data_tax_2_after_remove = data_tax_2_after_remove[['hadm_id']]
        data_tax_3_after_remove = data_tax_3_after_remove[['hadm_id']]
        join0 = pd.merge(data_tax_1_after_remove,data_tax_2_after_remove,on='hadm_id',how='inner')
        join1 = pd.merge(join0,data_tax_3_after_remove,on='hadm_id',how='inner')
        join = pd.merge(labeled_data,join1,on='hadm_id',how='inner')

        return join
    
    def join_data_4_tax(data_cm,data_pcs,data_drg,data_hcpcs,labeled_data):
        data_cm_after_remove = Preprocesser.remove_patients_with_many_codes(data_cm)
        data_pcs_after_remove = Preprocesser.remove_patients_with_many_codes(data_pcs)
        data_drg_after_remove = Preprocesser.remove_patients_with_many_codes(data_drg)
        data_hcpcs_after_remove = Preprocesser.remove_patients_with_many_codes(data_hcpcs)
        data_cm_after_remove = data_cm_after_remove[['hadm_id']]
        data_pcs_after_remove = data_pcs_after_remove[['hadm_id']]
        data_drg_after_remove = data_drg_after_remove[['hadm_id']]
        data_hcpcs_after_remove = data_hcpcs_after_remove[['hadm_id']]
        join0 = pd.merge(data_cm_after_remove,data_pcs_after_remove,on='hadm_id',how='inner')
        join1 = pd.merge(join0,data_drg_after_remove,on='hadm_id',how='inner')
        join2 = pd.merge(join1,data_hcpcs_after_remove,on='hadm_id',how='inner')
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
    

    def find_k_using_cv(data, train_distance_matrix):

        X = pd.DataFrame(train_distance_matrix)
        y = data['curr_service']

        # Define a range of k values to test
        k_values = range(1, 21)

        # We will use Stratified K-Fold to maintain the proportion of each class in each fold
        cv = StratifiedKFold(n_splits=5)

        # Dictionary to store the average weighted F1 scores for each k value
        f1_scores = {}

        for k in k_values:
            model = KNeighborsClassifier(n_neighbors=k)

            # Calculate cross-validated weighted F1 score for each k
            scores = cross_val_score(model, X, y, cv=cv, scoring=make_scorer(f1_score, average='weighted'))
            
            # Store the average F1 score
            f1_scores[k] = np.mean(scores)

        # Filter out k values that are less than or equal to 2
        filtered_f1_scores = {k: score for k, score in f1_scores.items() if k > 2}

        best_k = max(filtered_f1_scores, key=lambda k: (filtered_f1_scores[k], k))

        print(f"The best k value with the highest weighted F1-score is: {best_k}")

        return best_k