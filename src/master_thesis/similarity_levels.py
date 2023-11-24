from functools import reduce
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import min_weight_full_bipartite_matching
import math

from master_thesis.simple_icd_10_pcs import SimpleIcd10Pcs
from master_thesis.hcpcs import Hcpcs

class BaseSimilarityLevels:
    """parameters used for IC,CS,SS formulas"""
    def __init__(self, simple_icd_10_class) -> None:
        self.tax = simple_icd_10_class()

    def get_ancestors(self, concept: str) -> list[str]:
        """get ancestors of a concept"""
        ancestors = (self.tax.get_ancestors(concept))
        return ancestors

    def get_num_levels(self, concept: str) -> int:
        """get levels of a concept (same as IC#1)"""
        levels = len(self.get_ancestors(concept))+1
        return levels

    def get_num_subsumers(self, concept: str) -> int:
        """get number of subsumers/ancestors of a concept"""
        subsumer = len(self.get_ancestors(concept)) + 1
        return subsumer

    def get_leaves_of_root(self, ) -> list[str]:
        """get concepts of leaves for the root node (r) of the taxonomy"""
        all_codes = self.tax.get_all_codes()
        leaves = []
        for c in all_codes:
            if self.tax.is_leaf(c) == True:
                leaves.append(c)
        return leaves

    def get_num_leaves_of_root(self, ) -> int:
        """get number of leaves for the root node (r) of the taxonomy"""
        # workarounf to make process faster:
        if type(self.tax) == SimpleIcd10Pcs:
            return 78136
        elif type(self.tax) == Hcpcs:
            return 7372
        # End of workaround
        leaves_num = len(self.get_leaves_of_root())
        return leaves_num

    def get_num_of_leaves(self, concept: str) -> int:
        """get number of leaves for a concept"""
        # workarounf to make process faster:
        if type(self.tax) == SimpleIcd10Pcs:
            return self.tax.get_num_of_leaves_pcs(concept)
        # End of workaround
        descendants = self.tax.get_descendants(concept)
        leaves = 0
        for c in descendants:
            if self.tax.is_leaf(c) == True:
                leaves = leaves+1
        return leaves

    def get_concept_with_total_levels_in_taxonomy(self) -> str:
        """get total levels in the taxonomy"""
        # workarounf to make process faster:
        if type(self.tax) == SimpleIcd10Pcs:
            return '0TTB4ZZ'
        if type(self.tax) == Hcpcs:
            return 'A4206'
        # End of workaround
        leaves_of_root = self.get_leaves_of_root()
        list_levels = []
        for leaf in leaves_of_root:
            leaf_level = self.get_num_levels(leaf)
            list_levels.append(leaf_level)
        total_levels = max(list_levels)
        a=list_levels.index(total_levels)
        concept_with_most_levels = leaves_of_root[a]
        return concept_with_most_levels

    def get_details(self, patient_list: list[list[str]]):
        """get details of list of patients with concepts"""
        print(f'Numer of patients: {len(patient_list)}')
        for c in patient_list:
            print('patient#:',patient_list.index(c)+1, '\tnumber of concepts:',len(c))
            for n in c:
                print('\tconcept', c.index(n)+1,':',  n, '\tlevels:',self.get_num_levels(n), '\tancestors:',self.get_ancestors(n))

    def get_average(self, list: list[float]) -> float:
        """get average of a list"""
        return reduce(lambda a, b: a + b, list) / len(list)

    def get_average_list_of_lists(self, list_of_lists: list[list[float]]) -> list[float]:
        """get average of each list in list of lists"""
        new_list = []
        for i in list_of_lists:
            average = self.get_average(i)
            new_list.append(average)
        return new_list

    def get_lca(self, concept1: str,concept2: str) -> str:
        """get least common ancestor (LCA) for between 2 concepts"""
        lca = self.tax.get_nearest_common_ancestor(concept1,concept2)
        if lca == '':
            print(concept1,concept2,'\tlevels of LCA: 0', '\tleast common ancestor is the root node')
            return None
        if concept1==concept2:
            print(concept1,concept2,f'\tlevels of LCA: {self.get_num_levels(lca)}', '\tEXACT CONCEPT!')
        else:
            print(concept1,concept2,f'\tlevels of LCA: {self.get_num_levels(lca)}', f'\tleast common ancestor: {lca}')
        return lca


class SimilarityLevels(BaseSimilarityLevels):
    # ============ IC =============
    def get_ic1(self, concept: str) -> int:
        """get IC#1 of a concept (same as levels)"""
        if concept == None:
            return 0
        levels = len(self.get_ancestors(concept))+1
        return levels

    def get_ic2(self,concept: str) -> float:
        """get IC#2 of a concept"""
        if concept == None:
            return 0
        in_log = ((self.get_num_of_leaves(concept)/self.get_num_subsumers(concept))+1)/(self.get_num_leaves_of_root()+1)
        ic2 = - math.log(in_log, 10)
        return ic2

    # ============ CS =============
    def get_cs1(self,concept1: str,concept2: str,ic_function) -> float:
        """get Code level similarity CS#1 between 2 concepts"""
        cs1 = 1 - ((2*ic_function(self.get_lca(concept1,concept2)))/ (ic_function(concept1) + ic_function(concept2)))
        print('CS#1 =',cs1)
        return cs1

    def get_cs2(self,concept1: str,concept2: str,ic_function) -> float:
        """get Code level similarity CS#2 between 2 concepts"""
        cs2 = (ic_function(self.get_concept_with_total_levels_in_taxonomy()) - ic_function(self.get_lca(concept1,concept2)))/ic_function(self.get_concept_with_total_levels_in_taxonomy())
        print('CS#2 =',cs2)
        return cs2

    # ========compare CS===========
    def compareCS(self,patients_list: list[list[str]],ic_function,cs_function) -> float:
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
    def get_ss1(self,patient1: list[str],patient2: list[str],ic_function,cs_function) -> float:
        """get Set level similarity SS#1 between 2 patients (2 sets of concepts) using min"""
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
        ss1 = (sum1+sum2)/(len(A)+len(B))
        print(f'SS#1: {ss1}')
        return ss1

    def get_ss2(self,patient1: list[str],patient2: list[str],ic_function,cs_function) -> float:
        """get Set level similarity SS#2 between 2 patients (2 sets of concepts)"""
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
        ss2 = total/len(AUB)
        print(f'SS#2: {ss2}')
        return ss2

    def get_ss3(self,patient1: list[str],patient2: list[str],ic_function,cs_function) -> float:
        """get Set level similarity SS#3 between 2 patients (2 sets of concepts)"""
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
        ss3 = summ/(len(A)*len(B))
        print(f'SS#3: {ss3}')
        return ss3

    def get_ss4(self,patient1: list[str],patient2: list[str],ic_function,cs_function) -> float:
        """get Set level similarity SS#4 Minimum Weighted Bipartite Matching between 2 patients"""
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
        ss4 = sumCs/min(len(A),len(B))
        print(f'weight(CS) of edges with a minimum sum of weights(CS): {new_list}')
        print(f'SS#4: {ss4}')
        return ss4
