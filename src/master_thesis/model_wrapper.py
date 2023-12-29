class ModelWrapper:
    """Train/Test"""
    @staticmethod
    def get_distance_matrix(patients_list: list[list[str]],ic_function,cs_function,ss_funtion) -> list[list[float]]:
        """get distance matrix from list of patients"""
        n=1
        matrix = []
        for index1, p1 in enumerate(patients_list):
            row = []
            for index2, p2 in enumerate(patients_list):
                if index1 == index2:
                    index2 + 1
                    row.append(0)
                    continue
                if index1 > index2:
                    row.append(int(str(index1)+str(index2)))
                    continue
                print(f'(Case:{n}, Patients: first_patient: {index1+1}, second_patient: {index2+1})')
                n=n+1
                set_level_similarity = ss_funtion(p1,p2,ic_function,cs_function)
                print(set_level_similarity)
                row.append(set_level_similarity)
            matrix.append(row)

        end = len(matrix)
        for i in range(0,end):
            for j in range(0,end):
                if i > j:
                    matrix[i][j] = matrix[j][i]
        return matrix

    @staticmethod
    def get_test_distance(patients_list_1: list[list[str]],patients_list_2: list[list[str]],ic_function,cs_function,ss_funtion) -> list[list[float]]:
        """get distance between train patients and test patients"""
        n=1
        matrix = []
        for index1, p1 in enumerate(patients_list_1):
            row = []
            for index2, p2 in enumerate(patients_list_2):
                print(f'(Case:{n}, Patients: first_patient: {index1+1}, second_patient: {index2+1})')
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
