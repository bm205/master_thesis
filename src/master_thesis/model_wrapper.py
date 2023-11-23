class ModelWrapper:
    """Train/Test"""
    @staticmethod
    def get_distance_matrix(patients_list: list[list[str]],ic_function,cs_function,ss_funtion) -> list[list[float]]:
        """get distance matrix from list of patients"""
        n=1
        matrix = []
        for p1 in patients_list:
            row = []
            for p2 in patients_list:
                if patients_list.index(p1) == patients_list.index(p2):
                    patients_list.index(p2) + 1
                    row.append(0)
                    continue
                print(f'(Case:{n}, Patients: first_patient: {patients_list.index(p1)+1}, second_patient: {patients_list.index(p2)+1})')
                n=n+1
                set_level_similarity = ss_funtion(p1,p2,ic_function,cs_function)
                print(set_level_similarity)
                row.append(set_level_similarity)
            matrix.append(row)
        return matrix

    @staticmethod
    def get_test_distance(patients_list_1: list[list[str]],patients_list_2: list[list[str]],ic_function,cs_function,ss_funtion) -> list[list[float]]:
        """get distance between train patients and test patients"""
        n=1
        matrix = []
        for p1 in patients_list_1:
            row = []
            for p2 in patients_list_2:
                print(f'(Case:{n}, Patients: first_patient: {patients_list_1.index(p1)+1}, second_patient: {patients_list_2.index(p2)+1})')
                n=n+1
                set_level_similarity = ss_funtion(p1,p2,ic_function,cs_function)
                print(set_level_similarity)
                row.append(set_level_similarity)
            matrix.append(row)
        return matrix

    @staticmethod
    def get_y(patients_list) -> list[str]:
        """get labels of training data (train_patients)"""
        y_labels = []
        for _, row in patients_list.iterrows():
            if row['seq_num'] == 1:
                y_labels.append(row['curr_service'])
        print(y_labels)
        return y_labels
