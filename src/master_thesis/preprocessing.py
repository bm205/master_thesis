import pandas as pd
import numpy as np
import master_thesis.config as config

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
        previous_service = ''
        last = len(services['curr_service']) - 1
        for index,row in services.iterrows():
            if index == last:
                break
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

        filtered_services.to_csv('data/service_filtered.csv')
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
    
    def join_cm_pcs_drg():
        data_cm = pd.read_csv('data/diagnoses_icd.csv')
        data_cm = Preprocesser.filtering_icd(data_cm)
        data_pcs = pd.read_csv('data/procedures_icd.csv')
        data_pcs = Preprocesser.filtering_icd(data_pcs)
        data_drg = pd.read_csv('data/drg_to_icd.csv')
        data_cm_after_remove = Preprocesser.remove_patients_with_many_codes(data_cm)
        data_pcs_after_remove = Preprocesser.remove_patients_with_many_codes(data_pcs)
        data_drg_after_remove = Preprocesser.remove_patients_with_many_codes(data_drg)
        data_cm_after_remove = data_cm_after_remove[['hadm_id']]
        data_pcs_after_remove = data_pcs_after_remove[['hadm_id']]
        data_drg_after_remove = data_drg_after_remove[['hadm_id']]
        data_service = pd.read_csv('data/services_filtered.csv')
        data_service = data_service[['hadm_id','curr_service']]
        join0 = pd.merge(data_cm_after_remove,data_pcs_after_remove,on='hadm_id',how='inner')
        join1 = pd.merge(join0,data_drg_after_remove,on='hadm_id',how='inner')
        join = pd.merge(data_service,join1,on='hadm_id',how='inner')

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
        