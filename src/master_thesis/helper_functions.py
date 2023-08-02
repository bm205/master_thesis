import master_thesis.simple_icd_10_cm as cm
import pandas as pd
import numpy as np
from functools import reduce
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import min_weight_full_bipartite_matching
import math

def get_ancestors(concept: str) -> list[str]:
    """get ancestors of a concept"""
    ancestors = (cm.get_ancestors(concept))
    return ancestors

def get_num_levels(concept: str) -> int:
    """get levels of a concept (same as IC#1)"""
    levels = len(get_ancestors(concept))+1
    return levels

def get_num_subsumers(concept: str) -> int:
    """get number of subsumers/ancestors of a concept"""
    subsumer = len(get_ancestors(concept)) + 1
    return subsumer

def get_leaves_of_root() -> list[str]:
    """get concepts of leaves for the root node (r) of the taxonomy"""
    all_codes = cm.get_all_codes()
    leaves = []
    for c in all_codes:
        if cm.is_leaf(c) == True:
            leaves.append(c)
    return leaves

def get_num_leaves_of_root() -> int:
    """get number of leaves for the root node (r) of the taxonomy"""
    leaves_num = len(get_leaves_of_root())
    return leaves_num

def get_num_of_leaves(concept: str) -> int:
    """get number of leaves for a concept"""
    descendants = cm.get_descendants(concept)
    leaves = 0
    for c in descendants:
        if cm.is_leaf(c) == True:
            leaves = leaves+1
    return leaves

def get_concept_with_total_levels_in_taxonomy() -> str:
    """get total levels in the taxonomy"""
    leaves_of_root = get_leaves_of_root()
    list_levels = []
    for leaf in leaves_of_root:
        leaf_level = get_num_levels(leaf)
        list_levels.append(leaf_level)
    total_levels = max(list_levels)
    a=list_levels.index(total_levels)
    concept_with_most_levels = leaves_of_root[a]
    return concept_with_most_levels

def get_details(patient_list: list[list[str]]):
    """get details of list of patients with concepts"""
    print(f'Numer of patients: {len(patient_list)}')
    for c in patient_list:
        print('patient#:',patient_list.index(c)+1, '\tnumber of concepts:',len(c))
        for n in c:
            print('\tconcept', c.index(n)+1,':',  n, '\tlevels:',get_num_levels(n), '\tancestors:',get_ancestors(n))

def get_average(list: list[float]) -> float:
    """get average of a list"""
    return reduce(lambda a, b: a + b, list) / len(list)

def get_average_list_of_lists(list_of_lists: list[list[float]]) -> list[float]:
    """get average of each list in list of lists"""
    new_list = []
    for i in list_of_lists:
        average = get_average(i)
        new_list.append(average)
    return new_list

def get_lca(concept1: str,concept2: str) -> str:
    """get least common ancestor (LCA) for between 2 concepts"""
    lca = cm.get_nearest_common_ancestor(concept1,concept2)
    if lca == '':
        print(concept1,concept2,'\tlevels of LCA: 0', '\tleast common ancestor is the root node')
        return None
    if concept1==concept2:
        print(concept1,concept2,f'\tlevels of LCA: {get_num_levels(lca)}', '\tEXACT CONCEPT!')
    else:
        print(concept1,concept2,f'\tlevels of LCA: {get_num_levels(lca)}', f'\tleast common ancestor: {lca}')
    return lca


# ============ IC =============

def get_ic1(concept: str) -> int:
    """get IC#1 of a concept (same as levels)"""
    if concept == None:
        return 0
    levels = len(get_ancestors(concept))+1
    return levels

def get_ic2(concept: str) -> float:
    """get IC#2 of a concept"""
    if concept == None:
        return 0
    in_log = ((get_num_of_leaves(concept)/get_num_subsumers(concept))+1)/(get_num_leaves_of_root()+1)
    ic2 = - math.log(in_log, 10)
    return ic2


# ============ CS =============

def get_cs2(concept1: str,concept2: str,ic_function) -> float:
    """get Code level similarity CS#2 between 2 concepts"""
    cs2 = 1 - ((2*ic_function(get_lca(concept1,concept2)))/ (ic_function(concept1) + ic_function(concept2)))
    print('cs#2 =',cs2)
    return cs2

def get_cs4(concept1: str,concept2: str,ic_function) -> float:
    """get Code level similarity CS#4 between 2 concepts"""
    cs4 = (ic_function(get_concept_with_total_levels_in_taxonomy()) - ic_function(get_lca(concept1,concept2)))/ic_function(get_concept_with_total_levels_in_taxonomy())
    print('cs#4 =',cs4)
    return cs4

# ============================

# compare CS
def compareCS(patients_list: list[list[str]],ic_function,cs_function) -> float:
    n=1
    for c1 in patients_list:
        for c2 in patients_list:
            if patients_list.index(c1) >= patients_list.index(c2):
                patients_list.index(c2) + 1
                continue
            for n1 in c1:
                for n2 in c2:
                    print(f'({n})')
                    n=n+1
                    cs_function(n1,n2,ic_function)


# ============ SS =============

def get_ss5(patient1: list[str],patient2: list[str],ic_function,cs_function) -> float:
    """get Set level similarity SS#5 between 2 patients (2 sets of concepts)"""
    A = patient1
    B = patient2
    n=1
    csCom = []
    for a in A:
        csComunit = []
        for b in B:
            print(f'({n}): concepts: first_patient_concept: {A.index(a)+1}, second_patient_concept: {B.index(b)+1}')
            n=n+1
            csSimilarity = cs_function(a,b,ic_function)
            csComunit.append(csSimilarity)
        print(f'CS for each concept of first patient: {csComunit}')
        minn = min(csComunit)
        csCom.append(minn)
    print(f'Min CSs of concepts of first patient: {csCom}')
    sum1 = sum(csCom)
    csCom = []
    for b in B:
        csComunit = []
        for a in A:
            print(f'({n}): concepts: second_patient_concept: {B.index(b)+1}, first_patient_concept: {A.index(a)+1}')
            n=n+1
            csSimilarity = cs_function(b,a,ic_function)
            csComunit.append(csSimilarity)
        print(f'CS for each concept of second patient: {csComunit}')
        minn = min(csComunit)
        csCom.append(minn)
    print(f'Min CS\'s of concepts of second patient: {csCom}')
    sum2 = sum(csCom)
    ss5 = (sum1+sum2)/(len(A)+len(B))
    print(f'SS#5: {ss5}')
    return ss5

def get_ss6(patient1: list[str],patient2: list[str],ic_function,cs_function) -> float:
    """get Set level similarity SS#6 between 2 patients (2 sets of concepts)"""
    A = set(patient1)
    B = set(patient2)
    AUB = A | B
    AdiffB = A - B
    BdiffA = B - A
    n=1
    csCom = []
    for a in AdiffB:
        summ = 0
        for b in B:
            print(f'({n}): concepts: first_patient_concept: {patient1.index(a)+1}, second_patient_concept: {patient2.index(b)+1}')
            n=n+1
            csSimilarity = cs_function(a,b,ic_function)
            summ = summ + csSimilarity
        total1= summ/len(B)
        csCom.append(total1)
    for b in BdiffA:
        summ = 0
        for a in A:
            print(f'({n}): concepts: second_patient_concept: {patient2.index(b)+1}, first_patient_concept: {patient1.index(a)+1}')
            n=n+1
            csSimilarity = cs_function(b,a,ic_function)
            summ = summ + csSimilarity
        total2=summ/len(patient1)
        csCom.append(total2)
    print(f'Average CS\'s of each concept of first and second patients: {csCom}')
    total = sum(csCom)
    print(AUB)
    ss6 = total/len(AUB)
    print(f'SS#6: {ss6}')
    return ss6

def get_ss7(patient1: list[str],patient2: list[str],ic_function,cs_function) -> float:
    """get Set level similarity SS#7 between 2 patients (2 sets of concepts)"""
    A = patient1
    B = patient2
    n=1
    summ = 0
    for a in A:
        for b in B:
            print(f'({n}): concepts: first_patient_concept: {A.index(a)+1}, second_patient_concept: {B.index(b)+1}')
            n=n+1
            csSimilarity = cs_function(a,b,ic_function)
            summ = summ + csSimilarity
    ss7 = summ/(len(A)*len(B))
    print(f'SS#7: {ss7}')
    return ss7

def get_ss8(patient1: list[str],patient2: list[str],ic_function,cs_function) -> float:
    """get Set level similarity SS#8 Minimum Weighted Bipartite Matching between 2 patients"""
    A = set(patient1)
    B = set(patient2)
    AdiffB = A - B
    BdiffA = B - A
    n=1
    csCom = []
    if len(AdiffB) <= len(BdiffA):
        start = AdiffB
        end = BdiffA
        start_draft = patient1
        end_draft = patient2
        first_patient = 'first_patient_concept:'
        second_patient = 'second_patient_concept:'
    else:
        start = BdiffA
        end = AdiffB
        start_draft = patient2
        end_draft = patient1
        first_patient = 'second_patient_concept:'
        second_patient = 'first_patient_concept:'
    for c1 in start:
        csComunit = []
        for c2 in end:
            print(f'({n}): concepts: {first_patient} {start_draft.index(c1)+1}, {second_patient} {end_draft.index(c2)+1}')
            n=n+1
            csSimilarity = cs_function(c1,c2,ic_function)
            csComunit.append(csSimilarity)
        csCom.append(csComunit)
    print(f'Disjoint concepts of A and B: {AdiffB, BdiffA}')
    print(f'CS of concepts: {csCom}')
    biadjacency_matrix = csr_matrix(csCom)
    indecies = min_weight_full_bipartite_matching(biadjacency_matrix)[1]
    new_list = []
    print(f'Subset of edges with a minimum sum of weights(CS): {indecies}')
    for xx in csCom:
        dd = xx[indecies[csCom.index(xx)]]
        new_list.append(dd)
    sumCs = sum(new_list)
    ss8 = sumCs/min(len(A),len(B))
    print(f'weight(CS) of edges with a minimum sum of weights(CS): {new_list}')
    print(f'SS#8: {ss8}')
    return ss8

def get_similarity(patients_list: list[list[str]],ic_function,cs_function,ss_funtion) -> list[list[float]]:
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

def get_test_distance(patients_list_1: list[list[str]],patients_list_2: list[list[str]],ic_function,cs_function,ss_funtion) -> list[list[float]]:
    """get distance matrix between train patients and test patients"""
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

# ================ Preprocessing ===========

def get_patients(patients_list):
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
            while True:
                try:
                    get_ancestors(c)
                    break
                except ValueError:
                    print(i)
                    print(c)
                    patients_filtered[i] = ''
                    print("Oops!  This code is not valid in the taxonomy...")
                    break
        i= i+1
    
    while patients_filtered.__contains__(''):
        patients_filtered.remove('')

    patients_filtered_num = len(patients_filtered)
    print(patients_filtered)
    print(patients_filtered_num)
    return patients_filtered

# ==============

def get_y_train(patients_list):
    """get labels of training data (train_patients)"""
    y_labels = []
    for index, row in patients_list.iterrows():
        if row['seq_num'] == 1:
            y_labels.append(row['curr_service'])
    print(y_labels)
    return y_labels

