import pandas as pd



class BaseSimpleIcd10Pcs:
    def __init__(self):
        self.taxonomy = {}
        self.add_node(None, "origin")

    def add_node(self, parent_id, code):
        if parent_id not in self.taxonomy:
            self.taxonomy[parent_id] = []
        self.taxonomy[parent_id].append(code)

    def is_valid_item(self, code):
        for children in self.taxonomy.values():
            for child in children:
                if child == code:
                    return True
        return False
    
    def is_leaf(self, code):
        if self.is_valid_item(code) != True:
            raise ValueError("The code \""+code+"\" does not exist.")
        if self.get_children(code) == []:
            return True
        else:
            return False
        
    def get_all_codes(self):
        all_codes_list = []
        for children in self.taxonomy.values():
            for child in children:
                all_codes_list.append(child)
        return all_codes_list           

    def get_children(self, code):
        if self.is_valid_item(code) != True:
            raise ValueError("The code \""+code+"\" does not exist.")
        return self.taxonomy.get(code, [])
    
    def get_ancestors(self, code):
        ancestors = []
        if self.is_valid_item(code) != True:
            raise ValueError("The code \""+code+"\" does not exist.")
        while code is not None:
            for parent_id, children in self.taxonomy.items():
                for child in children:
                    if child == code and parent_id != None:
                        ancestors.append(parent_id)
                        code = parent_id
                        break
                else:
                    continue
                break
            else:
                break
        return ancestors
        
    def get_descendants(self, code):
        if self.is_valid_item(code) != True:
            raise ValueError("The code \""+code+"\" does not exist.")
        descendants = []
        def find_descendants(code):
            if code in self.taxonomy:
                for child in self.taxonomy[code]:
                    descendants.append(child)
                    find_descendants(child)

        find_descendants(code)
        return descendants


class SimpleIcd10Pcs(BaseSimpleIcd10Pcs):
    def __init__(self):
        super().__init__()
        self.populate_taxonomy()

    def get_nearest_common_ancestor(self, a:str,b:str) -> str:
        anc_a = [a] + self.get_ancestors(a)
        anc_b = [b] + self.get_ancestors(b)
        if len(anc_b) > len(anc_a):
            temp = anc_a
            anc_a = anc_b
            anc_b = temp
        for anc in anc_a:
            if anc in anc_b:
                return anc
        return ""
    
    def populate_taxonomy(self):
        df = pd.read_csv('./src/master_thesis/taxonomies/icd10pcs_order_20211.csv')
        df2 = df.loc[df['Column3'] == 1]
        col2 = df2[['Column2']]

        sections_1 = set()
        level_1 = []
        i=-1

        for _, row in col2.iterrows():
            section = row['Column2'][0]
            if section not in sections_1:
                sections_1.add(section)
                self.add_node("origin", f"Section {section}")
                level_1.append([])
                i = i + 1
            level_1[i].append(row['Column2'])


        level_2_0 = []

        for a in level_1:
            i=-1
            sections_2 = set()
            level_2 = []
            for b in a:
                section_1 = b[0]
                section_2 = b[1]
                if section_2 not in sections_2:
                    sections_2.add(section_2)
                    self.add_node(f"Section {section_1}", f"Section {section_1 + section_2}")
                    level_2.append([])
                    i = i + 1
                level_2[i].append(b)
            level_2_0.append(level_2)

        level_3_0 = []

        for a in level_2_0:
            for c in a:
                i=-1
                sections_3 = set()
                level_3 = []
                for b in c:
                    section_1 = b[0]
                    section_2 = b[1]
                    section_3 = b[2]
                    if section_3 not in sections_3:
                        sections_3.add(section_3)
                        self.add_node(f"Section {section_1 + section_2}", f"Section {section_1 + section_2 + section_3}")
                        level_3.append([])
                        i = i + 1
                    level_3[i].append(b)
                level_3_0.append(level_3)

        level_4_0 = []

        for a in level_3_0:
            for c in a:
                i=-1
                sections_4 = set()
                level_4 = []
                for b in c:
                    section_1 = b[0]
                    section_2 = b[1]
                    section_3 = b[2]
                    section_4 = b[3]
                    if section_4 not in sections_4:
                        sections_4.add(section_4)
                        self.add_node(f"Section {section_1 + section_2 + section_3}", f"Section {section_1 + section_2 + section_3 + section_4}")
                        level_4.append([])
                        i = i + 1
                    level_4[i].append(b)
                level_4_0.append(level_4)

        level_5_0 = []

        for a in level_4_0:
            for c in a:
                i=-1
                sections_5 = set()
                level_5 = []
                for b in c:
                    section_1 = b[0]
                    section_2 = b[1]
                    section_3 = b[2]
                    section_4 = b[3]
                    section_5 = b[4]
                    if section_5 not in sections_5:
                        sections_5.add(section_5)
                        self.add_node(f"Section {section_1 + section_2 + section_3 + section_4}", f"Section {section_1 + section_2 + section_3 + section_4 + section_5}")
                        level_5.append([])
                        i = i + 1
                    level_5[i].append(b)
                level_5_0.append(level_5)

        level_6_0 = []

        for a in level_5_0:
            for c in a:
                i=-1
                sections_6 = set()
                level_6 = []
                for b in c:
                    section_1 = b[0]
                    section_2 = b[1]
                    section_3 = b[2]
                    section_4 = b[3]
                    section_5 = b[4]
                    section_6 = b[5]
                    if section_6 not in sections_6:
                        sections_6.add(section_6)
                        self.add_node(f"Section {section_1 + section_2 + section_3 + section_4 + section_5}",
                                        f"Section {section_1 + section_2 + section_3 + section_4 + section_5 + section_6}")
                        level_6.append([])
                        i = i + 1
                    level_6[i].append(b)
                level_6_0.append(level_6)

        level_7_0 = []

        for a in level_6_0:
            for c in a:
                i=-1
                sections_7 = set()
                level_7 = []
                for b in c:
                    section_1 = b[0]
                    section_2 = b[1]
                    section_3 = b[2]
                    section_4 = b[3]
                    section_5 = b[4]
                    section_6 = b[5]
                    section_7 = b[6]
                    if section_7 not in sections_7:
                        sections_7.add(section_7)
                        self.add_node(f"Section {section_1 + section_2 + section_3 + section_4 + section_5 + section_6}",
                                        f"{section_1 + section_2 + section_3 + section_4 + section_5 + section_6 + section_7}")
                        level_7.append([])
                        i = i + 1
                    level_7[i].append(b)
                level_7_0.append(level_7)

    def get_num_of_leaves_pcs(self, concept:str) -> int:
        df = pd.read_csv('./src/master_thesis/taxonomies/icd10pcs_order_20211.csv')
        df2 = df.loc[df['Column3'] == 1]
        col2 = df2[['Column2']]
        length = len(concept)
        cut = concept[8:length]
        if concept[0:7] == 'Section':
            count = col2[col2['Column2'].str.startswith(cut)]
            return len(count)
        else:
            return 0

if __name__ == "__main__":
    pcs = SimpleIcd10Pcs()
    # print(pcs.get_num_of_leaves_pcs('0TTB4ZZ'))
    
