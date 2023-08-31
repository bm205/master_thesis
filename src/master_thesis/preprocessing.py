class Preprocesser:
    """Preprocessing"""
    def __init__(self, simple_icd_10_class) -> None:
        self.cm = simple_icd_10_class()

    def get_patients(self, patients_list) -> list[list[str]]:
        """get list of concepts of patients & remove patients with not a valid concept"""
        patients = []
        for index, row in patients_list.iterrows():
            if row['seq_num'] == 1:
            # if row['seq_num']%4 == 0:
                patient = []
                patients.append(patient)
                patient.append(row['icd_code'])
            elif row['seq_num'] != 1 and patients == []:
                continue
            else: 
                patient.append(row['icd_code'])

        i = 0
        patients_filtered = patients.copy()
        for p in patients_filtered:
            for c in p:
                if self.cm.is_valid_item(c) == False:
                    print(i)
                    print(c)
                    patients_filtered[i] = ''
                    print("Oops!  This code is not valid in the taxonomy...")
                    break
                else:
                    continue
            i= i+1
        
        while patients_filtered.__contains__(''):
            patients_filtered.remove('')

        patients_filtered_num = len(patients_filtered)
        print(patients_filtered)
        print(patients_filtered_num)
        return patients_filtered
