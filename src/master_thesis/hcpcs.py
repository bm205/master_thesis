import pandas as pd



class BaseHcpcs:
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


class Hcpcs(BaseHcpcs):
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
        df = pd.read_csv('./src/master_thesis/taxonomies/hcpcs_codes_2023.csv')
        col2 = df[['HCPC']]

        self.add_node("origin", "A0021-A0999")
        self.add_node("origin", "A2001-A2025")
        self.add_node("origin", "A4100-A4100")
        self.add_node("origin", "A4206-A8004")
        self.add_node("origin", "A9150-A9999")
        self.add_node("origin", "B4034-B9999")
        self.add_node("origin", "C1052-C1062")
        self.add_node("origin", "C1713-C9899")
        self.add_node("origin", "E0100-E8002")
        self.add_node("origin", "G0008-G9987")
        self.add_node("origin", "H0001-H2037")
        self.add_node("origin", "J0120-J8999")
        self.add_node("origin", "J9000-J9999")
        self.add_node("origin", "K0001-K0900")
        self.add_node("origin", "K1001-K1036")
        self.add_node("origin", "L0112-L4631")
        self.add_node("origin", "L5000-L9900")
        self.add_node("origin", "M0001-M0005")
        self.add_node("origin", "M0010-M0010")
        self.add_node("origin", "M0075-M0301")
        self.add_node("origin", "M1003-M1070")
        self.add_node("origin", "M1106-M1143")
        self.add_node("origin", "M1146-M1210")
        self.add_node("origin", "P2028-P9615")
        self.add_node("origin", "Q0035-Q9992")
        self.add_node("origin", "R0070-R0076")
        self.add_node("origin", "S0012-S9999")
        self.add_node("origin", "T1000-T5999")
        self.add_node("origin", "U0001-U0005")
        self.add_node("origin", "V2020-V2799")
        self.add_node("origin", "V5008-V5364")
        self.add_node("origin", "HCPCS-MODIFIERS")

        self.add_node("A4206-A8004", "A4206-A4232")
        self.add_node("A4206-A8004", "A4233-A4239")
        self.add_node("A4206-A8004", "A4244-A4290")
        self.add_node("A4206-A8004", "A4300-A4306")
        self.add_node("A4206-A8004", "A4310-A4360")
        self.add_node("A4206-A8004", "A4361-A4437")
        self.add_node("A4206-A8004", "A4450-A4608")
        self.add_node("A4206-A8004", "A4611-A4629")
        self.add_node("A4206-A8004", "A4630-A4640")
        self.add_node("A4206-A8004", "A4641-A4642")
        self.add_node("A4206-A8004", "A4648-A4652")
        self.add_node("A4206-A8004", "A4653-A4932")
        self.add_node("A4206-A8004", "A5051-A5093")
        self.add_node("A4206-A8004", "A5102-A5200")
        self.add_node("A4206-A8004", "A5500-A5514")
        self.add_node("A4206-A8004", "A6000-A6208")
        self.add_node("A4206-A8004", "A6209-A6215")
        self.add_node("A4206-A8004", "A6216-A6233")
        self.add_node("A4206-A8004", "A6234-A6241")
        self.add_node("A4206-A8004", "A6242-A6248")
        self.add_node("A4206-A8004", "A6250-A6412")
        self.add_node("A4206-A8004", "A6413-A6461")
        self.add_node("A4206-A8004", "A6501-A6550")
        self.add_node("A4206-A8004", "A6590-A6591")
        self.add_node("A4206-A8004", "A7000-A7049")
        self.add_node("A4206-A8004", "A7501-A7527")
        self.add_node("A4206-A8004", "A8000-A8004")

        self.add_node("A9150-A9999", "A9150-A9300")
        self.add_node("A9150-A9999", "A9500-A9800")
        self.add_node("A9150-A9999", "A9900-A9999")

        self.add_node("B4034-B9999", "B4034-B4088")
        self.add_node("B4034-B9999", "B4100-B4162")
        self.add_node("B4034-B9999", "B4164-B5200")
        self.add_node("B4034-B9999", "B9002-B9999")

        self.add_node("C1713-C9899", "C1713-C1715")
        self.add_node("C1713-C9899", "C1716-C1719")
        self.add_node("C1713-C9899", "C1721-C1722")
        self.add_node("C1713-C9899", "C1724-C1759")
        self.add_node("C1713-C9899", "C1760-C2615")
        self.add_node("C1713-C9899", "C2616-C2616")
        self.add_node("C1713-C9899", "C2617-C2631")
        self.add_node("C1713-C9899", "C2634-C2699")
        self.add_node("C1713-C9899", "C5271-C5278")
        self.add_node("C1713-C9899", "C7500-C7555")
        self.add_node("C1713-C9899", "C7900-C7902")
        self.add_node("C1713-C9899", "C8900-C8920")
        self.add_node("C1713-C9899", "C8921-C8930")
        self.add_node("C1713-C9899", "C8931-C8936")
        self.add_node("C1713-C9899", "C8937-C8937")
        self.add_node("C1713-C9899", "C8957-C9488")
        self.add_node("C1713-C9899", "C9507-C9507")
        self.add_node("C1713-C9899", "C9600-C9608")
        self.add_node("C1713-C9899", "C9725-C9899")

        self.add_node("E0100-E8002", "E0100-E0159")
        self.add_node("E0100-E8002", "E0160-E0162")
        self.add_node("E0100-E8002", "E0163-E0175")
        self.add_node("E0100-E8002", "E0181-E0199")
        self.add_node("E0100-E8002", "E0200-E0239")
        self.add_node("E0100-E8002", "E0240-E0249")
        self.add_node("E0100-E8002", "E0250-E0373")
        self.add_node("E0100-E8002", "E0424-E0491")
        self.add_node("E0100-E8002", "E0500-E0500")
        self.add_node("E0100-E8002", "E0550-E0601")
        self.add_node("E0100-E8002", "E0602-E0604")
        self.add_node("E0100-E8002", "E0605-E0606")
        self.add_node("E0100-E8002", "E0607-E0620")
        self.add_node("E0100-E8002", "E0621-E0642")
        self.add_node("E0100-E8002", "E0650-E0677")
        self.add_node("E0100-E8002", "E0691-E0694")
        self.add_node("E0100-E8002", "E0700-E0711")
        self.add_node("E0100-E8002", "E0720-E0770")
        self.add_node("E0100-E8002", "E0776-E0791")
        self.add_node("E0100-E8002", "E0830-E0948")
        self.add_node("E0100-E8002", "E0950-E1036")
        self.add_node("E0100-E8002", "E1037-E1039")
        self.add_node("E0100-E8002", "E1050-E1070")
        self.add_node("E0100-E8002", "E1083-E1086")
        self.add_node("E0100-E8002", "E1087-E1090")
        self.add_node("E0100-E8002", "E1092-E1093")
        self.add_node("E0100-E8002", "E1100-E1110")
        self.add_node("E0100-E8002", "E1130-E1161")
        self.add_node("E0100-E8002", "E1170-E1200")
        self.add_node("E0100-E8002", "E1220-E1228")
        self.add_node("E0100-E8002", "E1229-E1239")
        self.add_node("E0100-E8002", "E1240-E1270")
        self.add_node("E0100-E8002", "E1280-E1298")
        self.add_node("E0100-E8002", "E1300-E1310")
        self.add_node("E0100-E8002", "E1352-E1406")
        self.add_node("E0100-E8002", "E1500-E1699")
        self.add_node("E0100-E8002", "E1700-E1702")
        self.add_node("E0100-E8002", "E1800-E1841")
        self.add_node("E0100-E8002", "E1902-E1902")
        self.add_node("E0100-E8002", "E2000-E2120")
        self.add_node("E0100-E8002", "E1905-E1905")
        self.add_node("E0100-E8002", "E2201-E2295")
        self.add_node("E0100-E8002", "E2300-E2398")
        self.add_node("E0100-E8002", "E2402-E2402")
        self.add_node("E0100-E8002", "E2500-E2599")
        self.add_node("E0100-E8002", "E2601-E2625")
        self.add_node("E0100-E8002", "E2626-E2633")
        self.add_node("E0100-E8002", "E8000-E8002")

        self.add_node("G0008-G9987", "G0008-G0010") 
        self.add_node("G0008-G9987", "G0027-G0027") 
        self.add_node("G0008-G9987", "G0028-G0067") 
        self.add_node("G0008-G9987", "G0068-G0070") 
        self.add_node("G0008-G9987", "G0071-G0071") 
        self.add_node("G0008-G9987", "G0076-G0087") 
        self.add_node("G0008-G9987", "G0088-G0090") 
        self.add_node("G0008-G9987", "G0101-G0124") 
        self.add_node("G0008-G9987", "G0127-G0372") 
        self.add_node("G0008-G9987", "G0378-G0384") 
        self.add_node("G0008-G9987", "G0390-G0390") 
        self.add_node("G0008-G9987", "G0396-G0397") 
        self.add_node("G0008-G9987", "G0398-G0400") 
        self.add_node("G0008-G9987", "G0402-G0405") 
        self.add_node("G0008-G9987", "G0406-G0408") 
        self.add_node("G0008-G9987", "G0409-G0411") 
        self.add_node("G0008-G9987", "G0412-G0415") 
        self.add_node("G0008-G9987", "G0416-G0416") 
        self.add_node("G0008-G9987", "G0420-G0421") 
        self.add_node("G0008-G9987", "G0422-G0424") 
        self.add_node("G0008-G9987", "G0425-G0427") 
        self.add_node("G0008-G9987", "G0428-G0429") 
        self.add_node("G0008-G9987", "G0432-G0435") 
        self.add_node("G0008-G9987", "G0438-G0451") 
        self.add_node("G0008-G9987", "G0452-G0465") 
        self.add_node("G0008-G9987", "G0466-G0470") 
        self.add_node("G0008-G9987", "G0471-G0659") 
        self.add_node("G0008-G9987", "G0913-G0918") 
        self.add_node("G0008-G9987", "G1001-G1028") 
        self.add_node("G0008-G9987", "G2000-G2000") 
        self.add_node("G0008-G9987", "G2001-G2020") 
        self.add_node("G0008-G9987", "G2021-G2025") 
        self.add_node("G0008-G9987", "G2066-G2066") 
        self.add_node("G0008-G9987", "G2067-G2075") 
        self.add_node("G0008-G9987", "G2076-G2081") 
        self.add_node("G0008-G9987", "G2082-G2083") 
        self.add_node("G0008-G9987", "G2086-G2088") 
        self.add_node("G0008-G9987", "G2090-G2152") 
        self.add_node("G0008-G9987", "G2167-G2167") 
        self.add_node("G0008-G9987", "G2168-G2169") 
        self.add_node("G0008-G9987", "G2172-G2172") 
        self.add_node("G0008-G9987", "G2173-G2210") 
        self.add_node("G0008-G9987", "G2211-G2214") 
        self.add_node("G0008-G9987", "G2215-G2216") 
        self.add_node("G0008-G9987", "G2250-G2250") 
        self.add_node("G0008-G9987", "G2251-G2252") 
        self.add_node("G0008-G9987", "G3002-G3003") 
        self.add_node("G0008-G9987", "G4000-G4038") 
        self.add_node("G0008-G9987", "G6001-G6017") 
        self.add_node("G0008-G9987", "G8395-G8635") 
        self.add_node("G0008-G9987", "G8647-G8670") 
        self.add_node("G0008-G9987", "G8694-G8970") 
        self.add_node("G0008-G9987", "G9001-G9012") 
        self.add_node("G0008-G9987", "G9013-G9140") 
        self.add_node("G0008-G9987", "G9143-G9143") 
        self.add_node("G0008-G9987", "G9147-G9147") 
        self.add_node("G0008-G9987", "G9148-G9153") 
        self.add_node("G0008-G9987", "G9156-G9156") 
        self.add_node("G0008-G9987", "G9157-G9157") 
        self.add_node("G0008-G9987", "G9187-G9187") 
        self.add_node("G0008-G9987", "G9188-G9893") 
        self.add_node("G0008-G9987", "G9894-G9897") 
        self.add_node("G0008-G9987", "G9898-G9898") 
        self.add_node("G0008-G9987", "G9899-G9900") 
        self.add_node("G0008-G9987", "G9901-G9901") 
        self.add_node("G0008-G9987", "G9902-G9909") 
        self.add_node("G0008-G9987", "G9910-G9910") 
        self.add_node("G0008-G9987", "G9911-G9911") 
        self.add_node("G0008-G9987", "G9912-G9915") 
        self.add_node("G0008-G9987", "G9916-G9918") 
        self.add_node("G0008-G9987", "G9919-G9932") 
        self.add_node("G0008-G9987", "G9938-G9940") 
        self.add_node("G0008-G9987", "G9942-G9949") 
        self.add_node("G0008-G9987", "G9954-G9961") 
        self.add_node("G0008-G9987", "G9962-G9963") 
        self.add_node("G0008-G9987", "G9964-G9970") 
        self.add_node("G0008-G9987", "G9974-G9975") 
        self.add_node("G0008-G9987", "G9978-G9987") 
        self.add_node("G0008-G9987", "G9988-G9999")

        self.add_node("H0001-H2037", "H0001-H0030") 
        self.add_node("H0001-H2037", "H0031-H0040")
        self.add_node("H0001-H2037", "H0041-H0042")
        self.add_node("H0001-H2037", "H0043-H0044")
        self.add_node("H0001-H2037", "H0045-H0050")
        self.add_node("H0001-H2037", "H1000-H1011")
        self.add_node("H0001-H2037", "H2000-H2041")

        self.add_node("J0120-J8999", "J0120-J7175")
        self.add_node("J0120-J8999", "J7177-J7214")
        self.add_node("J0120-J8999", "J7294-J7307")
        self.add_node("J0120-J8999", "J7308-J7402")
        self.add_node("J0120-J8999", "J7500-J7599")
        self.add_node("J0120-J8999", "J7604-J7686")
        self.add_node("J0120-J8999", "J7699-J8499")
        self.add_node("J0120-J8999", "J8501-J8999")

        self.add_node("K0001-K0900", "K0001-K0195")
        self.add_node("K0001-K0900", "K0455-K0605")
        self.add_node("K0001-K0900", "K0606-K0609")
        self.add_node("K0001-K0900", "K0669-K0746")
        self.add_node("K0001-K0900", "K0800-K0812")
        self.add_node("K0001-K0900", "K0813-K0899")
        self.add_node("K0001-K0900", "K0900-K0900")

        self.add_node("L0112-L4631", "L0112-L0174")
        self.add_node("L0112-L4631", "L0180-L0200")
        self.add_node("L0112-L4631", "L0220-L0220")
        self.add_node("L0112-L4631", "L0450-L0492")
        self.add_node("L0112-L4631", "L0621-L0624")
        self.add_node("L0112-L4631", "L0625-L0627")
        self.add_node("L0112-L4631", "L0628-L0640")
        self.add_node("L0112-L4631", "L0641-L0642")
        self.add_node("L0112-L4631", "L0643-L0651")
        self.add_node("L0112-L4631", "L0700-L0710")
        self.add_node("L0112-L4631", "L0810-L0861")
        self.add_node("L0112-L4631", "L0970-L0999")
        self.add_node("L0112-L4631", "L1000-L1120")
        self.add_node("L0112-L4631", "L1200-L1290")
        self.add_node("L0112-L4631", "L1300-L1499")
        self.add_node("L0112-L4631", "L1600-L1690")
        self.add_node("L0112-L4631", "L1700-L1755")
        self.add_node("L0112-L4631", "L1810-L1860")
        self.add_node("L0112-L4631", "L1900-L1990")
        self.add_node("L0112-L4631", "L2000-L2038")
        self.add_node("L0112-L4631", "L2040-L2090")
        self.add_node("L0112-L4631", "L2106-L2116")
        self.add_node("L0112-L4631", "L2126-L2136")
        self.add_node("L0112-L4631", "L2180-L2192")
        self.add_node("L0112-L4631", "L2200-L2397")
        self.add_node("L0112-L4631", "L2405-L2492")
        self.add_node("L0112-L4631", "L2500-L2550")
        self.add_node("L0112-L4631", "L2570-L2680")
        self.add_node("L0112-L4631", "L2750-L2999")
        self.add_node("L0112-L4631", "L3000-L3031")
        self.add_node("L0112-L4631", "L3040-L3090")
        self.add_node("L0112-L4631", "L3100-L3170")
        self.add_node("L0112-L4631", "L3201-L3207")
        self.add_node("L0112-L4631", "L3208-L3211")
        self.add_node("L0112-L4631", "L3212-L3214")
        self.add_node("L0112-L4631", "L3215-L3265")
        self.add_node("L0112-L4631", "L3300-L3334")
        self.add_node("L0112-L4631", "L3340-L3420")
        self.add_node("L0112-L4631", "L3430-L3485")
        self.add_node("L0112-L4631", "L3500-L3595")
        self.add_node("L0112-L4631", "L3600-L3649")
        self.add_node("L0112-L4631", "L3650-L3678")
        self.add_node("L0112-L4631", "L3702-L3762")
        self.add_node("L0112-L4631", "L3763-L3766")
        self.add_node("L0112-L4631", "L3806-L3904")
        self.add_node("L0112-L4631", "L3905-L3908")
        self.add_node("L0112-L4631", "L3912-L3956")
        self.add_node("L0112-L4631", "L3960-L3973")
        self.add_node("L0112-L4631", "L3975-L3978")
        self.add_node("L0112-L4631", "L3980-L3999")
        self.add_node("L0112-L4631", "L4000-L4210")
        self.add_node("L0112-L4631", "L4350-L4631")

        self.add_node("L5000-L9900", "L5000-L5020")
        self.add_node("L5000-L9900", "L5050-L5060")
        self.add_node("L5000-L9900", "L5100-L5105")
        self.add_node("L5000-L9900", "L5150-L5160")
        self.add_node("L5000-L9900", "L5200-L5230")
        self.add_node("L5000-L9900", "L5250-L5270")
        self.add_node("L5000-L9900", "L5280-L5341")
        self.add_node("L5000-L9900", "L5400-L5460")
        self.add_node("L5000-L9900", "L5500-L5505")
        self.add_node("L5000-L9900", "L5510-L5600")
        self.add_node("L5000-L9900", "L5610-L5617")
        self.add_node("L5000-L9900", "L5618-L5628")
        self.add_node("L5000-L9900", "L5629-L5653")
        self.add_node("L5000-L9900", "L5654-L5699")
        self.add_node("L5000-L9900", "L5700-L5703")
        self.add_node("L5000-L9900", "L5704-L5707")
        self.add_node("L5000-L9900", "L5710-L5780")
        self.add_node("L5000-L9900", "L5781-L5782")
        self.add_node("L5000-L9900", "L5785-L5795")
        self.add_node("L5000-L9900", "L5810-L5966")
        self.add_node("L5000-L9900", "L5968-L5999")
        self.add_node("L5000-L9900", "L6000-L6026")
        self.add_node("L5000-L9900", "L6050-L6055")
        self.add_node("L5000-L9900", "L6100-L6130")
        self.add_node("L5000-L9900", "L6200-L6205")
        self.add_node("L5000-L9900", "L6250-L6250")
        self.add_node("L5000-L9900", "L6300-L6320")
        self.add_node("L5000-L9900", "L6350-L6370")
        self.add_node("L5000-L9900", "L6380-L6388")
        self.add_node("L5000-L9900", "L6400-L6570")
        self.add_node("L5000-L9900", "L6580-L6590")
        self.add_node("L5000-L9900", "L6600-L6698")
        self.add_node("L5000-L9900", "L6703-L6882")
        self.add_node("L5000-L9900", "L6883-L6885")
        self.add_node("L5000-L9900", "L6890-L6915")
        self.add_node("L5000-L9900", "L6920-L6975")
        self.add_node("L5000-L9900", "L7007-L7045")
        self.add_node("L5000-L9900", "L7170-L7259")
        self.add_node("L5000-L9900", "L7360-L7368")
        self.add_node("L5000-L9900", "L7400-L7405")
        self.add_node("L5000-L9900", "L7499-L7499")
        self.add_node("L5000-L9900", "L7510-L7520")
        self.add_node("L5000-L9900", "L7600-L7600")
        self.add_node("L5000-L9900", "L7700-L7700")
        self.add_node("L5000-L9900", "L7900-L7902")
        self.add_node("L5000-L9900", "L8000-L8039")
        self.add_node("L5000-L9900", "L8040-L8049")
        self.add_node("L5000-L9900", "L8300-L8330")
        self.add_node("L5000-L9900", "L8400-L8485")
        self.add_node("L5000-L9900", "L8499-L8499")
        self.add_node("L5000-L9900", "L8500-L8515")
        self.add_node("L5000-L9900", "L8600-L8600")
        self.add_node("L5000-L9900", "L8603-L8607")
        self.add_node("L5000-L9900", "L8608-L8629")
        self.add_node("L5000-L9900", "L8630-L8659")
        self.add_node("L5000-L9900", "L8670-L8670")
        self.add_node("L5000-L9900", "L8678-L8689")
        self.add_node("L5000-L9900", "L8690-L9900")

        self.add_node("M1003-M1070", "M1003-M1005")
        self.add_node("M1003-M1070", "M1006-M1014")
        self.add_node("M1003-M1070", "M1016-M1018")
        self.add_node("M1003-M1070", "M1019-M1026")
        self.add_node("M1003-M1070", "M1027-M1031")
        self.add_node("M1003-M1070", "M1032-M1036")
        self.add_node("M1003-M1070", "M1037-M1041")
        self.add_node("M1003-M1070", "M1043-M1049")
        self.add_node("M1003-M1070", "M1051-M1051")
        self.add_node("M1003-M1070", "M1052-M1052")
        self.add_node("M1003-M1070", "M1054-M1054")
        self.add_node("M1003-M1070", "M1055-M1057")
        self.add_node("M1003-M1070", "M1058-M1060")
        self.add_node("M1003-M1070", "M1067-M1067")
        self.add_node("M1003-M1070", "M1068-M1068")
        self.add_node("M1003-M1070", "M1069-M1070")

        self.add_node("P2028-P9615", "P2028-P2038")
        self.add_node("P2028-P9615", "P3000-P3001")
        self.add_node("P2028-P9615", "P7001-P7001")
        self.add_node("P2028-P9615", "P9010-P9100")
        self.add_node("P2028-P9615", "P9603-P9604")
        self.add_node("P2028-P9615", "P9612-P9615")

        self.add_node("Q0035-Q9992", "Q0035-Q0144")
        self.add_node("Q0035-Q9992", "Q0161-Q0181")
        self.add_node("Q0035-Q9992", "Q0220-Q0249")
        self.add_node("Q0035-Q9992", "Q0477-Q0509")
        self.add_node("Q0035-Q9992", "Q0510-Q0514")
        self.add_node("Q0035-Q9992", "Q0515-Q2028")
        self.add_node("Q0035-Q9992", "Q2034-Q2039")
        self.add_node("Q0035-Q9992", "Q2041-Q3031")
        self.add_node("Q0035-Q9992", "Q4001-Q4051")
        self.add_node("Q0035-Q9992", "Q4074-Q4082")
        self.add_node("Q0035-Q9992", "Q4100-Q4286")
        self.add_node("Q0035-Q9992", "Q5001-Q5010")
        self.add_node("Q0035-Q9992", "Q5101-Q5101")
        self.add_node("Q0035-Q9992", "Q5103-Q5111")
        self.add_node("Q0035-Q9992", "Q5112-Q5131")
        self.add_node("Q0035-Q9992", "Q9001-Q9004")
        self.add_node("Q0035-Q9992", "Q9950-Q9983")
        self.add_node("Q0035-Q9992", "Q9991-Q9992")

        self.add_node("S0012-S9999", "S0012-S0197")
        self.add_node("S0012-S9999", "S0199-S0400")
        self.add_node("S0012-S9999", "S0500-S0596")
        self.add_node("S0012-S9999", "S0601-S0622")
        self.add_node("S0012-S9999", "S0630-S3722")
        self.add_node("S0012-S9999", "S3800-S3870")
        self.add_node("S0012-S9999", "S3900-S3904")
        self.add_node("S0012-S9999", "S4005-S4989")
        self.add_node("S0012-S9999", "S4990-S5014")
        self.add_node("S0012-S9999", "S5035-S5199")
        self.add_node("S0012-S9999", "S5497-S5523")
        self.add_node("S0012-S9999", "S5550-S5571")
        self.add_node("S0012-S9999", "S8030-S8092")
        self.add_node("S0012-S9999", "S8096-S8210")
        self.add_node("S0012-S9999", "S8265-S9152")
        self.add_node("S0012-S9999", "S9208-S9214")
        self.add_node("S0012-S9999", "S9325-S9379")
        self.add_node("S0012-S9999", "S9381-S9485")
        self.add_node("S0012-S9999", "S9490-S9810")
        self.add_node("S0012-S9999", "S9900-S9999")

        self.add_node("T1000-T5999", "T1000-T1005")
        self.add_node("T1000-T5999", "T1006-T1012")
        self.add_node("T1000-T5999", "T1013-T1018")
        self.add_node("T1000-T5999", "T1019-T1022")
        self.add_node("T1000-T5999", "T1023-T1029")
        self.add_node("T1000-T5999", "T1030-T1031")
        self.add_node("T1000-T5999", "T1032-T1033")
        self.add_node("T1000-T5999", "T1040-T1041")
        self.add_node("T1000-T5999", "T1502-T1999")
        self.add_node("T1000-T5999", "T2001-T2007")
        self.add_node("T1000-T5999", "T2010-T2011")
        self.add_node("T1000-T5999", "T2012-T2041")
        self.add_node("T1000-T5999", "T2042-T2046")
        self.add_node("T1000-T5999", "T2047-T2047")
        self.add_node("T1000-T5999", "T2048-T2048")
        self.add_node("T1000-T5999", "T2049-T2049")
        self.add_node("T1000-T5999", "T2050-T2051")
        self.add_node("T1000-T5999", "T2101-T2101")
        self.add_node("T1000-T5999", "T4521-T4545")
        self.add_node("T1000-T5999", "T5001-T5999")

        self.add_node("V2020-V2799", "V2020-V2025")
        self.add_node("V2020-V2799", "V2100-V2199")
        self.add_node("V2020-V2799", "V2200-V2299")
        self.add_node("V2020-V2799", "V2300-V2399")
        self.add_node("V2020-V2799", "V2410-V2499")
        self.add_node("V2020-V2799", "V2500-V2599")
        self.add_node("V2020-V2799", "V2600-V2615")
        self.add_node("V2020-V2799", "V2623-V2629")
        self.add_node("V2020-V2799", "V2630-V2632")
        self.add_node("V2020-V2799", "V2700-V2799")

        self.add_node("V5008-V5364", "V5008-V5020")
        self.add_node("V5008-V5364", "V5030-V5060")
        self.add_node("V5008-V5364", "V5070-V5110")
        self.add_node("V5008-V5364", "V5120-V5267")
        self.add_node("V5008-V5364", "V5268-V5290")
        self.add_node("V5008-V5364", "V5298-V5299")
        self.add_node("V5008-V5364", "V5336-V5364")


        for _, row in col2.iterrows():
            code_string= row['HCPC'][1]+row['HCPC'][2]+row['HCPC'][3]+row['HCPC'][4]
            code_int = int(code_string)
            if row['HCPC'][0] == 'A':
                if code_int >=21 and code_int <=999:
                    self.add_node("A0021-A0999", row['HCPC'])
                elif code_int >=2001 and code_int <=2025:
                    self.add_node("A2001-A2025", row['HCPC'])
                elif code_int >=4100 and code_int <=4100:
                    self.add_node("A4100-A4100", row['HCPC'])
                elif code_int >=9150 and code_int <=9300:
                    self.add_node("A9150-A9300", row['HCPC'])
                elif code_int >=9500 and code_int <=9800:
                    self.add_node("A9500-A9800", row['HCPC'])
                elif code_int >=9900 and code_int <=9999:
                    self.add_node("A9900-A9999", row['HCPC'])
                elif code_int >=4206 and code_int <=4232:
                    self.add_node("A4206-A4232", row['HCPC'])
                elif code_int >=4233 and code_int <=4239:
                    self.add_node("A4233-A4239", row['HCPC'])
                elif code_int >=4244 and code_int <=4290:
                    self.add_node("A4244-A4290", row['HCPC'])
                elif code_int >=4300 and code_int <=4306:
                    self.add_node("A4300-A4306", row['HCPC'])
                elif code_int >=4310 and code_int <=4360:
                    self.add_node("A4310-A4360", row['HCPC'])
                elif code_int >=4361 and code_int <=4437:
                    self.add_node("A4361-A4437", row['HCPC'])
                elif code_int >=4450 and code_int <=4608:
                    self.add_node("A4450-A4608", row['HCPC'])
                elif code_int >=4611 and code_int <=4629:
                    self.add_node("A4611-A4629", row['HCPC'])
                elif code_int >=4630 and code_int <=4642:
                    self.add_node("A4630-A4640", row['HCPC'])
                elif code_int >=4641 and code_int <=4652:
                    self.add_node("A4641-A4642", row['HCPC'])
                elif code_int >=4648 and code_int <=4932:
                    self.add_node("A4648-A4652", row['HCPC'])
                elif code_int >=4653 and code_int <=5039:
                    self.add_node("A4653-A4932", row['HCPC'])
                elif code_int >=5051 and code_int <=5200:
                    self.add_node("A5051-A5093", row['HCPC'])
                elif code_int >=5102 and code_int <=5514:
                    self.add_node("A5102-A5200", row['HCPC'])
                elif code_int >=6000 and code_int <=6208:
                    self.add_node("A6000-A6208", row['HCPC'])
                elif code_int >=6209 and code_int <=6215:
                    self.add_node("A6209-A6215", row['HCPC'])
                elif code_int >=6216 and code_int <=6233:
                    self.add_node("A6216-A6233", row['HCPC'])
                elif code_int >=6234 and code_int <=6241:
                    self.add_node("A6234-A6241", row['HCPC'])
                elif code_int >=6242 and code_int <=6248:
                    self.add_node("A6242-A6248", row['HCPC'])
                elif code_int >=6250 and code_int <=6412:
                    self.add_node("A6250-A6412", row['HCPC'])
                elif code_int >=6413 and code_int <=6461:
                    self.add_node("A6413-A6461", row['HCPC'])
                elif code_int >=6501 and code_int <=6550:
                    self.add_node("A6501-A6550", row['HCPC'])
                elif code_int >=6590 and code_int <=6591:
                    self.add_node("A6590-A6591", row['HCPC'])
                elif code_int >=7000 and code_int <=7049:
                    self.add_node("A7000-A7049", row['HCPC'])
                elif code_int >=7501 and code_int <=7527:
                    self.add_node("A7501-A7527", row['HCPC'])
                elif code_int >=8000 and code_int <=8004:
                    self.add_node("A8000-A8004", row['HCPC'])

            elif row['HCPC'][0] == 'B':
                if code_int >=4034 and code_int <=4088:    
                    self.add_node("B4034-B4088", row['HCPC'])
                elif code_int >=4100 and code_int <=4162:
                    self.add_node("B4100-B4162", row['HCPC'])
                elif code_int >=4141 and code_int <=5200:
                    self.add_node("B4164-B5200", row['HCPC'])
                elif code_int >=9002 and code_int <=9999:
                    self.add_node("B9002-B9999", row['HCPC'])

            elif row['HCPC'][0] == 'C':
                if code_int >=1052 and code_int <=1062:
                    self.add_node("C1052-C1062", row['HCPC'])
                elif code_int >=1713 and code_int <=1715:
                    self.add_node("C1713-C1715", row['HCPC'])
                elif code_int >=1716 and code_int <=1719:
                    self.add_node("C1716-C1719", row['HCPC'])
                elif code_int >=1721 and code_int <=1722:
                    self.add_node("C1721-C1722", row['HCPC'])
                elif code_int >=1724 and code_int <=1759:
                    self.add_node("C1724-C1759", row['HCPC'])
                elif code_int >=1760 and code_int <=2615:
                    self.add_node("C1760-C2615", row['HCPC'])
                elif code_int >=2616 and code_int <=2616:
                    self.add_node("C2616-C2616", row['HCPC'])
                elif code_int >=2617 and code_int <=2631:
                    self.add_node("C2617-C2631", row['HCPC'])
                elif code_int >=2634 and code_int <=2699:
                    self.add_node("C2634-C2699", row['HCPC'])
                elif code_int >=5271 and code_int <=5278:
                    self.add_node("C5271-C5278", row['HCPC'])
                elif code_int >=7500 and code_int <=7555:
                    self.add_node("C7500-C7555", row['HCPC'])
                elif code_int >=7900 and code_int <=7902:
                    self.add_node("C7900-C7902", row['HCPC'])
                elif code_int >=8900 and code_int <=8920:
                    self.add_node("C8900-C8920", row['HCPC'])
                elif code_int >=8921 and code_int <=8930:
                    self.add_node("C8921-C8930", row['HCPC'])
                elif code_int >=8931 and code_int <=8936:
                    self.add_node("C8931-C8936", row['HCPC'])
                elif code_int >=8937 and code_int <=8937:
                    self.add_node("C8937-C8937", row['HCPC'])
                elif code_int >=8957 and code_int <=9488:
                    self.add_node("C8957-C9488", row['HCPC'])
                elif code_int >=9507 and code_int <=9507:
                    self.add_node("C9507-C9507", row['HCPC'])
                elif code_int >=9600 and code_int <=9608:
                    self.add_node("C9600-C9608", row['HCPC'])
                elif code_int >=9725 and code_int <=9899:
                    self.add_node("C9725-C9899", row['HCPC'])

            elif row['HCPC'][0] == 'E':
                if code_int >=100 and code_int <=159:
                    self.add_node("E0100-E0159", row['HCPC'])
                elif code_int >=160 and code_int <=162:
                    self.add_node("E0160-E0162", row['HCPC'])
                elif code_int >=163 and code_int <=175:
                    self.add_node("E0163-E0175", row['HCPC'])
                elif code_int >=181 and code_int <=199:
                    self.add_node("E0181-E0199", row['HCPC'])
                elif code_int >=200 and code_int <=239:
                    self.add_node("E0200-E0239", row['HCPC'])
                elif code_int >=240 and code_int <=249:
                    self.add_node("E0240-E0249", row['HCPC'])
                elif code_int >=250 and code_int <=373:
                    self.add_node("E0250-E0373", row['HCPC'])
                elif code_int >=424 and code_int <=491:
                    self.add_node("E0424-E0491", row['HCPC'])
                elif code_int >=500 and code_int <=500:
                    self.add_node("E0500-E0500", row['HCPC'])
                elif code_int >=550 and code_int <=601:
                    self.add_node("E0550-E0601", row['HCPC'])
                elif code_int >=602 and code_int <=604:
                    self.add_node("E0602-E0604", row['HCPC'])
                elif code_int >=605 and code_int <=606:
                    self.add_node("E0605-E0606", row['HCPC'])
                elif code_int >=607 and code_int <=620:
                    self.add_node("E0607-E0620", row['HCPC'])
                elif code_int >=621 and code_int <=642:
                    self.add_node("E0621-E0642", row['HCPC'])
                elif code_int >=650 and code_int <=677:
                    self.add_node("E0650-E0677", row['HCPC'])
                elif code_int >=691 and code_int <=694:
                    self.add_node("E0691-E0694", row['HCPC'])
                elif code_int >=700 and code_int <=711:
                    self.add_node("E0700-E0711", row['HCPC'])
                elif code_int >=720 and code_int <=770:
                    self.add_node("E0720-E0770", row['HCPC'])
                elif code_int >=776 and code_int <=791:
                    self.add_node("E0776-E0791", row['HCPC'])
                elif code_int >=830 and code_int <=948:
                    self.add_node("E0830-E0948", row['HCPC'])
                elif code_int >=950 and code_int <=1036:
                    self.add_node("E0950-E1036", row['HCPC'])
                elif code_int >=1037 and code_int <=1039:
                    self.add_node("E1037-E1039", row['HCPC'])
                elif code_int >=1050 and code_int <=1070:
                    self.add_node("E1050-E1070", row['HCPC'])
                elif code_int >=1083 and code_int <=1086:
                    self.add_node("E1083-E1086", row['HCPC'])
                elif code_int >=1087 and code_int <=1090:
                    self.add_node("E1087-E1090", row['HCPC'])
                elif code_int >=1092 and code_int <=1093:
                    self.add_node("E1092-E1093", row['HCPC'])
                elif code_int >=1100 and code_int <=1110:
                    self.add_node("E1100-E1110", row['HCPC'])
                elif code_int >=1130 and code_int <=1161:
                    self.add_node("E1130-E1161", row['HCPC'])
                elif code_int >=1170 and code_int <=1200:
                    self.add_node("E1170-E1200", row['HCPC'])
                elif code_int >=1220 and code_int <=1228:
                    self.add_node("E1220-E1228", row['HCPC'])
                elif code_int >=1229 and code_int <=1239:
                    self.add_node("E1229-E1239", row['HCPC'])
                elif code_int >=1240 and code_int <=1270:
                    self.add_node("E1240-E1270", row['HCPC'])
                elif code_int >=1280 and code_int <=1298:
                    self.add_node("E1280-E1298", row['HCPC'])
                elif code_int >=1300 and code_int <=1310:
                    self.add_node("E1300-E1310", row['HCPC'])
                elif code_int >=1352 and code_int <=1406:
                    self.add_node("E1352-E1406", row['HCPC'])
                elif code_int >=1500 and code_int <=1699:
                    self.add_node("E1500-E1699", row['HCPC'])
                elif code_int >=1700 and code_int <=1702:
                    self.add_node("E1700-E1702", row['HCPC'])
                elif code_int >=1800 and code_int <=1841:
                    self.add_node("E1800-E1841", row['HCPC'])
                elif code_int >=1902 and code_int <=1902:
                    self.add_node("E1902-E1902", row['HCPC'])
                elif code_int >=2000 and code_int <=2120:
                    self.add_node("E2000-E2120", row['HCPC'])
                elif code_int >=1905 and code_int <=1905:
                    self.add_node("E1905-E1905", row['HCPC'])
                elif code_int >=2201 and code_int <=2295:
                    self.add_node("E2201-E2295", row['HCPC'])
                elif code_int >=2300 and code_int <=2398:
                    self.add_node("E2300-E2398", row['HCPC'])
                elif code_int >=2402 and code_int <=2402:
                    self.add_node("E2402-E2402", row['HCPC'])
                elif code_int >=2500 and code_int <=2599:
                    self.add_node("E2500-E2599", row['HCPC'])
                elif code_int >=2601 and code_int <=2625:
                    self.add_node("E2601-E2625", row['HCPC'])
                elif code_int >=2626 and code_int <=2633:
                    self.add_node("E2626-E2633", row['HCPC'])
                elif code_int >=8000 and code_int <=8002:
                    self.add_node("E8000-E8002", row['HCPC'])

            elif row['HCPC'][0] == 'G':
                if code_int >=8 and code_int <=10:
                    self.add_node("G0008-G0010", row['HCPC'])
                elif code_int >=27 and code_int <=27:
                    self.add_node("G0027-G0027", row['HCPC'])
                elif code_int >=28 and code_int <=67:
                    self.add_node("G0028-G0067", row['HCPC'])
                elif code_int >=68 and code_int <=70:
                    self.add_node("G0068-G0070", row['HCPC'])
                elif code_int >=71 and code_int <=71:
                    self.add_node("G0071-G0071", row['HCPC'])
                elif code_int >=76 and code_int <=87:
                    self.add_node("G0076-G0087", row['HCPC'])
                elif code_int >=88 and code_int <=90:
                    self.add_node("G0088-G0090", row['HCPC'])
                elif code_int >=101 and code_int <=124:
                    self.add_node("G0101-G0124", row['HCPC'])
                elif code_int >=127 and code_int <=372:
                    self.add_node("G0127-G0372", row['HCPC'])
                elif code_int >=378 and code_int <=384:
                    self.add_node("G0378-G0384", row['HCPC'])
                elif code_int >=390 and code_int <=390:
                    self.add_node("G0390-G0390", row['HCPC'])
                elif code_int >=396 and code_int <=397:
                    self.add_node("G0396-G0397", row['HCPC'])
                elif code_int >=398 and code_int <=400:
                    self.add_node("G0398-G0400", row['HCPC'])
                elif code_int >=402 and code_int <=405:
                    self.add_node("G0402-G0405", row['HCPC'])
                elif code_int >=406 and code_int <=408:
                    self.add_node("G0406-G0408", row['HCPC'])
                elif code_int >=409 and code_int <=411:
                    self.add_node("G0409-G0411", row['HCPC'])
                elif code_int >=412 and code_int <=415:
                    self.add_node("G0412-G0415", row['HCPC'])
                elif code_int >=416 and code_int <=416:
                    self.add_node("G0416-G0416", row['HCPC'])
                elif code_int >=420 and code_int <=421:
                    self.add_node("G0420-G0421", row['HCPC'])
                elif code_int >=422 and code_int <=424:
                    self.add_node("G0422-G0424", row['HCPC'])
                elif code_int >=425 and code_int <=427:
                    self.add_node("G0425-G0427", row['HCPC'])
                elif code_int >=428 and code_int <=429:
                    self.add_node("G0428-G0429", row['HCPC'])
                elif code_int >=432 and code_int <=435:
                    self.add_node("G0432-G0435", row['HCPC'])
                elif code_int >=438 and code_int <=451:
                    self.add_node("G0438-G0451", row['HCPC'])
                elif code_int >=452 and code_int <=465:
                    self.add_node("G0452-G0465", row['HCPC'])
                elif code_int >=466 and code_int <=470:
                    self.add_node("G0466-G0470", row['HCPC'])
                elif code_int >=471 and code_int <=659:
                    self.add_node("G0471-G0659", row['HCPC'])
                elif code_int >=913 and code_int <=918:
                    self.add_node("G0913-G0918", row['HCPC'])
                elif code_int >=1001 and code_int <=1028:
                    self.add_node("G1001-G1028", row['HCPC'])
                elif code_int >=2000 and code_int <=2000:
                    self.add_node("G2000-G2000", row['HCPC'])
                elif code_int >=2001 and code_int <=2020:
                    self.add_node("G2001-G2020", row['HCPC'])
                elif code_int >=2021 and code_int <=2025:
                    self.add_node("G2021-G2025", row['HCPC'])
                elif code_int >=2066 and code_int <=2066:
                    self.add_node("G2066-G2066", row['HCPC'])
                elif code_int >=2067 and code_int <=2075:
                    self.add_node("G2067-G2075", row['HCPC'])
                elif code_int >=2076 and code_int <=2081:
                    self.add_node("G2076-G2081", row['HCPC'])
                elif code_int >=2082 and code_int <=2083:
                    self.add_node("G2082-G2083", row['HCPC'])
                elif code_int >=2086 and code_int <=2088:
                    self.add_node("G2086-G2088", row['HCPC'])
                elif code_int >=2090 and code_int <=2152:
                    self.add_node("G2090-G2152", row['HCPC'])
                elif code_int >=2167 and code_int <=2167:
                    self.add_node("G2167-G2167", row['HCPC'])
                elif code_int >=2168 and code_int <=2169:
                    self.add_node("G2168-G2169", row['HCPC'])
                elif code_int >=2172 and code_int <=2172:
                    self.add_node("G2172-G2172", row['HCPC'])
                elif code_int >=2173 and code_int <=2210:
                    self.add_node("G2173-G2210", row['HCPC'])
                elif code_int >=2211 and code_int <=2214:
                    self.add_node("G2211-G2214", row['HCPC'])
                elif code_int >=2215 and code_int <=2216:
                    self.add_node("G2215-G2216", row['HCPC'])
                elif code_int >=2250 and code_int <=2250:
                    self.add_node("G2250-G2250", row['HCPC'])
                elif code_int >=2251 and code_int <=2252:
                    self.add_node("G2251-G2252", row['HCPC'])
                elif code_int >=3002 and code_int <=3003:
                    self.add_node("G3002-G3003", row['HCPC'])
                elif code_int >=4000 and code_int <=4038:
                    self.add_node("G4000-G4038", row['HCPC'])
                elif code_int >=6001 and code_int <=6017:
                    self.add_node("G6001-G6017", row['HCPC'])
                elif code_int >=8395 and code_int <=8635:
                    self.add_node("G8395-G8635", row['HCPC'])
                elif code_int >=8647 and code_int <=8670:
                    self.add_node("G8647-G8670", row['HCPC'])
                elif code_int >=8694 and code_int <=8970:
                    self.add_node("G8694-G8970", row['HCPC'])
                elif code_int >=9001 and code_int <=9012:
                    self.add_node("G9001-G9012", row['HCPC'])
                elif code_int >=9013 and code_int <=9140:
                    self.add_node("G9013-G9140", row['HCPC'])
                elif code_int >=9143 and code_int <=9143:
                    self.add_node("G9143-G9143", row['HCPC'])
                elif code_int >=9147 and code_int <=9147:
                    self.add_node("G9147-G9147", row['HCPC'])
                elif code_int >=9148 and code_int <=9153:
                    self.add_node("G9148-G9153", row['HCPC'])
                elif code_int >=9156 and code_int <=9156:
                    self.add_node("G9156-G9156", row['HCPC'])
                elif code_int >=9157 and code_int <=9157:
                    self.add_node("G9157-G9157", row['HCPC'])
                elif code_int >=9187 and code_int <=9187:
                    self.add_node("G9187-G9187", row['HCPC'])
                elif code_int >=9188 and code_int <=9893:
                    self.add_node("G9188-G9893", row['HCPC'])
                elif code_int >=9894 and code_int <=9897:
                    self.add_node("G9894-G9897", row['HCPC'])
                elif code_int >=9898 and code_int <=9898:
                    self.add_node("G9898-G9898", row['HCPC'])
                elif code_int >=9899 and code_int <=9900:
                    self.add_node("G9899-G9900", row['HCPC'])
                elif code_int >=9901 and code_int <=9901:
                    self.add_node("G9901-G9901", row['HCPC'])
                elif code_int >=9902 and code_int <=9909:
                    self.add_node("G9902-G9909", row['HCPC'])
                elif code_int >=9910 and code_int <=9910:
                    self.add_node("G9910-G9910", row['HCPC'])
                elif code_int >=9911 and code_int <=9911:
                    self.add_node("G9911-G9911", row['HCPC'])
                elif code_int >=9912 and code_int <=9915:
                    self.add_node("G9912-G9915", row['HCPC'])
                elif code_int >=9916 and code_int <=9918:
                    self.add_node("G9916-G9918", row['HCPC'])
                elif code_int >=9919 and code_int <=9932:
                    self.add_node("G9919-G9932", row['HCPC'])
                elif code_int >=9938 and code_int <=9940:
                    self.add_node("G9938-G9940", row['HCPC'])
                elif code_int >=9942 and code_int <=9949:
                    self.add_node("G9942-G9949", row['HCPC'])
                elif code_int >=9954 and code_int <=9961:
                    self.add_node("G9954-G9961", row['HCPC'])
                elif code_int >=9962 and code_int <=9963:
                    self.add_node("G9962-G9963", row['HCPC'])
                elif code_int >=9964 and code_int <=9970:
                    self.add_node("G9964-G9970", row['HCPC'])
                elif code_int >=9974 and code_int <=9975:
                    self.add_node("G9974-G9975", row['HCPC'])
                elif code_int >=9978 and code_int <=9987:
                    self.add_node("G9978-G9987", row['HCPC'])
                elif code_int >=9988 and code_int <=9999:
                    self.add_node("G9988-G9999", row['HCPC'])

            elif row['HCPC'][0] == 'H':
                if code_int >=1 and code_int <=30:
                    self.add_node("H0001-H0030", row['HCPC'])
                elif code_int >=31 and code_int <=40:
                    self.add_node("H0031-H0040", row['HCPC'])
                elif code_int >=41 and code_int <=42:
                    self.add_node("H0041-H0042", row['HCPC'])
                elif code_int >=43 and code_int <=44:
                    self.add_node("H0043-H0044", row['HCPC'])
                elif code_int >=45 and code_int <=50:
                    self.add_node("H0045-H0050", row['HCPC'])
                elif code_int >=1000 and code_int <=1011:
                    self.add_node("H1000-H1011", row['HCPC'])
                elif code_int >=2000 and code_int <=2041:
                    self.add_node("H2000-H2041", row['HCPC'])

            elif row['HCPC'][0] == 'J':
                if code_int >=120 and code_int <=7175:
                    self.add_node("J0120-J7175", row['HCPC'])
                elif code_int >=7177 and code_int <=7214:
                    self.add_node("J7177-J7214", row['HCPC'])
                elif code_int >=7294 and code_int <=7307:
                    self.add_node("J7294-J7307", row['HCPC'])
                elif code_int >=7308 and code_int <=7402:
                    self.add_node("J7308-J7402", row['HCPC'])
                elif code_int >=7500 and code_int <=7599:
                    self.add_node("J7500-J7599", row['HCPC'])
                elif code_int >=7604 and code_int <=7686:
                    self.add_node("J7604-J7686", row['HCPC'])
                elif code_int >=7699 and code_int <=8499:
                    self.add_node("J7699-J8499", row['HCPC'])
                elif code_int >=8501 and code_int <=8999:
                    self.add_node("J8501-J8999", row['HCPC'])
                elif code_int >=9000 and code_int <=9999:
                    self.add_node("J9000-J9999", row['HCPC'])

            elif row['HCPC'][0] == 'K':
                if code_int >=1 and code_int <=195:
                    self.add_node("K0001-K0195", row['HCPC'])
                elif code_int >=455 and code_int <=605:
                    self.add_node("K0455-K0605", row['HCPC'])
                elif code_int >=606 and code_int <=609:
                    self.add_node("K0606-K0609", row['HCPC'])
                elif code_int >=669 and code_int <=746:
                    self.add_node("K0669-K0746", row['HCPC'])
                elif code_int >=800 and code_int <=812:
                    self.add_node("K0800-K0812", row['HCPC'])
                elif code_int >=813 and code_int <=899:
                    self.add_node("K0813-K0899", row['HCPC'])
                elif code_int >=900 and code_int <=900:
                    self.add_node("K0900-K0900", row['HCPC'])
                elif code_int >=1001 and code_int <=1036:
                    self.add_node("K1001-K1036", row['HCPC'])

            elif row['HCPC'][0] == 'L':
                if code_int >=112 and code_int <=174:
                    self.add_node("L0112-L0174", row['HCPC'])
                elif code_int >=180 and code_int <=200:
                    self.add_node("L0180-L0200", row['HCPC'])
                elif code_int >=220 and code_int <=220:
                    self.add_node("L0220-L0220", row['HCPC'])
                elif code_int >=450 and code_int <=492:
                    self.add_node("L0450-L0492", row['HCPC'])
                elif code_int >=621 and code_int <=624:
                    self.add_node("L0621-L0624", row['HCPC'])
                elif code_int >=625 and code_int <=627:
                    self.add_node("L0625-L0627", row['HCPC'])
                elif code_int >=628 and code_int <=640:
                    self.add_node("L0628-L0640", row['HCPC'])
                elif code_int >=641 and code_int <=642:
                    self.add_node("L0641-L0642", row['HCPC'])
                elif code_int >=643 and code_int <=651:
                    self.add_node("L0643-L0651", row['HCPC'])
                elif code_int >=700 and code_int <=710:
                    self.add_node("L0700-L0710", row['HCPC'])
                elif code_int >=810 and code_int <=861:
                    self.add_node("L0810-L0861", row['HCPC'])
                elif code_int >=970 and code_int <=999:
                    self.add_node("L0970-L0999", row['HCPC'])
                elif code_int >=1000 and code_int <=1120:
                    self.add_node("L1000-L1120", row['HCPC'])
                elif code_int >=1200 and code_int <=1290:
                    self.add_node("L1200-L1290", row['HCPC'])
                elif code_int >=1300 and code_int <=1499:
                    self.add_node("L1300-L1499", row['HCPC'])
                elif code_int >=1600 and code_int <=1690:
                    self.add_node("L1600-L1690", row['HCPC'])
                elif code_int >=1700 and code_int <=1755:
                    self.add_node("L1700-L1755", row['HCPC'])
                elif code_int >=1810 and code_int <=1860:
                    self.add_node("L1810-L1860", row['HCPC'])
                elif code_int >=1900 and code_int <=1990:
                    self.add_node("L1900-L1990", row['HCPC'])
                elif code_int >=2000 and code_int <=2038:
                    self.add_node("L2000-L2038", row['HCPC'])
                elif code_int >=2040 and code_int <=2090:
                    self.add_node("L2040-L2090", row['HCPC'])
                elif code_int >=2106 and code_int <=2116:
                    self.add_node("L2106-L2116", row['HCPC'])
                elif code_int >=2126 and code_int <=2136:
                    self.add_node("L2126-L2136", row['HCPC'])
                elif code_int >=2180 and code_int <=2192:
                    self.add_node("L2180-L2192", row['HCPC'])
                elif code_int >=2200 and code_int <=2397:
                    self.add_node("L2200-L2397", row['HCPC'])
                elif code_int >=2405 and code_int <=2492:
                    self.add_node("L2405-L2492", row['HCPC'])
                elif code_int >=2500 and code_int <=2550:
                    self.add_node("L2500-L2550", row['HCPC'])
                elif code_int >=2570 and code_int <=2680:
                    self.add_node("L2570-L2680", row['HCPC'])
                elif code_int >=2750 and code_int <=2999:
                    self.add_node("L2750-L2999", row['HCPC'])
                elif code_int >=3000 and code_int <=3031:
                    self.add_node("L3000-L3031", row['HCPC'])
                elif code_int >=3040 and code_int <=3090:
                    self.add_node("L3040-L3090", row['HCPC'])
                elif code_int >=3100 and code_int <=3170:
                    self.add_node("L3100-L3170", row['HCPC'])
                elif code_int >=3201 and code_int <=3207:
                    self.add_node("L3201-L3207", row['HCPC'])
                elif code_int >=3208 and code_int <=3211:
                    self.add_node("L3208-L3211", row['HCPC'])
                elif code_int >=3212 and code_int <=3214:
                    self.add_node("L3212-L3214", row['HCPC'])
                elif code_int >=3215 and code_int <=3265:
                    self.add_node("L3215-L3265", row['HCPC'])
                elif code_int >=3300 and code_int <=3334:
                    self.add_node("L3300-L3334", row['HCPC'])
                elif code_int >=3340 and code_int <=3420:
                    self.add_node("L3340-L3420", row['HCPC'])
                elif code_int >=3430 and code_int <=3485:
                    self.add_node("L3430-L3485", row['HCPC'])
                elif code_int >=3500 and code_int <=3595:
                    self.add_node("L3500-L3595", row['HCPC'])
                elif code_int >=3600 and code_int <=3649:
                    self.add_node("L3600-L3649", row['HCPC'])
                elif code_int >=3650 and code_int <=3678:
                    self.add_node("L3650-L3678", row['HCPC'])
                elif code_int >=3702 and code_int <=3762:
                    self.add_node("L3702-L3762", row['HCPC'])
                elif code_int >=3763 and code_int <=3766:
                    self.add_node("L3763-L3766", row['HCPC'])
                elif code_int >=3806 and code_int <=3904:
                    self.add_node("L3806-L3904", row['HCPC'])
                elif code_int >=3905 and code_int <=3908:
                    self.add_node("L3905-L3908", row['HCPC'])
                elif code_int >=3912 and code_int <=3956:
                    self.add_node("L3912-L3956", row['HCPC'])
                elif code_int >=3960 and code_int <=3973:
                    self.add_node("L3960-L3973", row['HCPC'])
                elif code_int >=3975 and code_int <=3978:
                    self.add_node("L3975-L3978", row['HCPC'])
                elif code_int >=3980 and code_int <=3999:
                    self.add_node("L3980-L3999", row['HCPC'])
                elif code_int >=4000 and code_int <=4210:
                    self.add_node("L4000-L4210", row['HCPC'])
                elif code_int >=4350 and code_int <=4631:
                    self.add_node("L4350-L4631", row['HCPC'])
                elif code_int >=5000 and code_int <=5020:
                    self.add_node("L5000-L5020", row['HCPC'])
                elif code_int >=5050 and code_int <=5060:
                    self.add_node("L5050-L5060", row['HCPC'])
                elif code_int >=5100 and code_int <=5105:
                    self.add_node("L5100-L5105", row['HCPC'])
                elif code_int >=5150 and code_int <=5160:
                    self.add_node("L5150-L5160", row['HCPC'])
                elif code_int >=5200 and code_int <=5230:
                    self.add_node("L5200-L5230", row['HCPC'])
                elif code_int >=5250 and code_int <=5270:
                    self.add_node("L5250-L5270", row['HCPC'])
                elif code_int >=5280 and code_int <=5341:
                    self.add_node("L5280-L5341", row['HCPC'])
                elif code_int >=5400 and code_int <=5460:
                    self.add_node("L5400-L5460", row['HCPC'])
                elif code_int >=5500 and code_int <=5505:
                    self.add_node("L5500-L5505", row['HCPC'])
                elif code_int >=5510 and code_int <=5600:
                    self.add_node("L5510-L5600", row['HCPC'])
                elif code_int >=5610 and code_int <=5617:
                    self.add_node("L5610-L5617", row['HCPC'])
                elif code_int >=5618 and code_int <=5628:
                    self.add_node("L5618-L5628", row['HCPC'])
                elif code_int >=5629 and code_int <=5653:
                    self.add_node("L5629-L5653", row['HCPC'])
                elif code_int >=5654 and code_int <=5699:
                    self.add_node("L5654-L5699", row['HCPC'])
                elif code_int >=5700 and code_int <=5703:
                    self.add_node("L5700-L5703", row['HCPC'])
                elif code_int >=5704 and code_int <=5707:
                    self.add_node("L5704-L5707", row['HCPC'])
                elif code_int >=5710 and code_int <=5780:
                    self.add_node("L5710-L5780", row['HCPC'])
                elif code_int >=5781 and code_int <=5782:
                    self.add_node("L5781-L5782", row['HCPC'])
                elif code_int >=5785 and code_int <=5795:
                    self.add_node("L5785-L5795", row['HCPC'])
                elif code_int >=5810 and code_int <=5966:
                    self.add_node("L5810-L5966", row['HCPC'])
                elif code_int >=5968 and code_int <=5999:
                    self.add_node("L5968-L5999", row['HCPC'])
                elif code_int >=6000 and code_int <=6026:
                    self.add_node("L6000-L6026", row['HCPC'])
                elif code_int >=6050 and code_int <=6055:
                    self.add_node("L6050-L6055", row['HCPC'])
                elif code_int >=6100 and code_int <=6130:
                    self.add_node("L6100-L6130", row['HCPC'])
                elif code_int >=6200 and code_int <=6205:
                    self.add_node("L6200-L6205", row['HCPC'])
                elif code_int >=6250 and code_int <=6250:
                    self.add_node("L6250-L6250", row['HCPC'])
                elif code_int >=6300 and code_int <=6320:
                    self.add_node("L6300-L6320", row['HCPC'])
                elif code_int >=6350 and code_int <=6370:
                    self.add_node("L6350-L6370", row['HCPC'])
                elif code_int >=6380 and code_int <=6388:
                    self.add_node("L6380-L6388", row['HCPC'])
                elif code_int >=6400 and code_int <=6570:
                    self.add_node("L6400-L6570", row['HCPC'])
                elif code_int >=6580 and code_int <=6590:
                    self.add_node("L6580-L6590", row['HCPC'])
                elif code_int >=6600 and code_int <=6698:
                    self.add_node("L6600-L6698", row['HCPC'])
                elif code_int >=6703 and code_int <=6882:
                    self.add_node("L6703-L6882", row['HCPC'])
                elif code_int >=6883 and code_int <=6885:
                    self.add_node("L6883-L6885", row['HCPC'])
                elif code_int >=6890 and code_int <=6915:
                    self.add_node("L6890-L6915", row['HCPC'])
                elif code_int >=6920 and code_int <=6975:
                    self.add_node("L6920-L6975", row['HCPC'])
                elif code_int >=7007 and code_int <=7045:
                    self.add_node("L7007-L7045", row['HCPC'])
                elif code_int >=7170 and code_int <=7259:
                    self.add_node("L7170-L7259", row['HCPC'])
                elif code_int >=7360 and code_int <=7368:
                    self.add_node("L7360-L7368", row['HCPC'])
                elif code_int >=7400 and code_int <=7405:
                    self.add_node("L7400-L7405", row['HCPC'])
                elif code_int >=7499 and code_int <=7499:
                    self.add_node("L7499-L7499", row['HCPC'])
                elif code_int >=7510 and code_int <=7520:
                    self.add_node("L7510-L7520", row['HCPC'])
                elif code_int >=7600 and code_int <=7600:
                    self.add_node("L7600-L7600", row['HCPC'])
                elif code_int >=7700 and code_int <=7700:
                    self.add_node("L7700-L7700", row['HCPC'])
                elif code_int >=7900 and code_int <=7902:
                    self.add_node("L7900-L7902", row['HCPC'])
                elif code_int >=8000 and code_int <=8039:
                    self.add_node("L8000-L8039", row['HCPC'])
                elif code_int >=8040 and code_int <=8049:
                    self.add_node("L8040-L8049", row['HCPC'])
                elif code_int >=8300 and code_int <=8330:
                    self.add_node("L8300-L8330", row['HCPC'])
                elif code_int >=8400 and code_int <=8485:
                    self.add_node("L8400-L8485", row['HCPC'])
                elif code_int >=8499 and code_int <=8499:
                    self.add_node("L8499-L8499", row['HCPC'])
                elif code_int >=8500 and code_int <=8515:
                    self.add_node("L8500-L8515", row['HCPC'])
                elif code_int >=8600 and code_int <=8600:
                    self.add_node("L8600-L8600", row['HCPC'])
                elif code_int >=8603 and code_int <=8607:
                    self.add_node("L8603-L8607", row['HCPC'])
                elif code_int >=8608 and code_int <=8629:
                    self.add_node("L8608-L8629", row['HCPC'])
                elif code_int >=8630 and code_int <=8659:
                    self.add_node("L8630-L8659", row['HCPC'])
                elif code_int >=8670 and code_int <=8670:
                    self.add_node("L8670-L8670", row['HCPC'])
                elif code_int >=8678 and code_int <=8689:
                    self.add_node("L8678-L8689", row['HCPC'])
                elif code_int >=8690 and code_int <=9900:
                    self.add_node("L8690-L9900", row['HCPC'])

            elif row['HCPC'][0] == 'M':
                if code_int <=5:
                    self.add_node("M0001-M0005", row['HCPC'])
                elif code_int >=10 and code_int <=10:
                    self.add_node("M0010-M0010", row['HCPC'])
                elif code_int >=75 and code_int <=301:
                    self.add_node("M0075-M0301", row['HCPC'])
                elif code_int <=1143 and code_int >=1106:
                    self.add_node("M1106-M1143", row['HCPC'])
                elif code_int <=1210 and code_int >=1146:
                    self.add_node("M1146-M1210", row['HCPC'])
                elif code_int >=1003 and code_int <=1005:
                    self.add_node("M1003-M1005", row['HCPC'])
                elif code_int >=1006 and code_int <=1014:
                    self.add_node("M1006-M1014", row['HCPC'])
                elif code_int >=1016 and code_int <=1018:
                    self.add_node("M1016-M1018", row['HCPC'])
                elif code_int >=1019 and code_int <=1026:
                    self.add_node("M1019-M1026", row['HCPC'])
                elif code_int >=1027 and code_int <=1031:
                    self.add_node("M1027-M1031", row['HCPC'])
                elif code_int >=1032 and code_int <=1036:
                    self.add_node("M1032-M1036", row['HCPC'])
                elif code_int >=1037 and code_int <=1041:
                    self.add_node("M1037-M1041", row['HCPC'])
                elif code_int >=1043 and code_int <=1049:
                    self.add_node("M1043-M1049", row['HCPC'])
                elif code_int >=1051 and code_int <=1051:
                    self.add_node("M1051-M1051", row['HCPC'])
                elif code_int >=1052 and code_int <=1052:
                    self.add_node("M1052-M1052", row['HCPC'])
                elif code_int >=1054 and code_int <=1054:
                    self.add_node("M1054-M1054", row['HCPC'])
                elif code_int >=1055 and code_int <=1057:
                    self.add_node("M1055-M1057", row['HCPC'])
                elif code_int >=1058 and code_int <=1060:
                    self.add_node("M1058-M1060", row['HCPC'])
                elif code_int >=1067 and code_int <=1067:
                    self.add_node("M1067-M1067", row['HCPC'])
                elif code_int >=1068 and code_int <=1068:
                    self.add_node("M1068-M1068", row['HCPC'])
                elif code_int >=1069 and code_int <=1070:
                    self.add_node("M1069-M1070", row['HCPC'])

            elif row['HCPC'][0] == 'P':
                if code_int >=2028 and code_int <=2038:
                    self.add_node("P2028-P2038", row['HCPC'])
                elif code_int >=3000 and code_int <=3001:
                    self.add_node("P3000-P3001", row['HCPC'])
                elif code_int >=7001 and code_int <=7001:
                    self.add_node("P7001-P7001", row['HCPC'])
                elif code_int >=9010 and code_int <=9100:
                    self.add_node("P9010-P9100", row['HCPC'])
                elif code_int >=9603 and code_int <=9604:
                    self.add_node("P9603-P9604", row['HCPC'])
                elif code_int >=9612 and code_int <=9615:
                    self.add_node("P9612-P9615", row['HCPC'])

            elif row['HCPC'][0] == 'Q':
                if code_int >=35 and code_int <=144:
                    self.add_node("Q0035-Q0144", row['HCPC'])
                elif code_int >=161 and code_int <=181:
                    self.add_node("Q0161-Q0181", row['HCPC'])
                elif code_int >=220 and code_int <=249:
                    self.add_node("Q0220-Q0249", row['HCPC'])
                elif code_int >=477 and code_int <=509:
                    self.add_node("Q0477-Q0509", row['HCPC'])
                elif code_int >=510 and code_int <=514:
                    self.add_node("Q0510-Q0514", row['HCPC'])
                elif code_int >=515 and code_int <=2028:
                    self.add_node("Q0515-Q2028", row['HCPC'])
                elif code_int >=2034 and code_int <=2039:
                    self.add_node("Q2034-Q2039", row['HCPC'])
                elif code_int >=2041 and code_int <=3031:
                    self.add_node("Q2041-Q3031", row['HCPC'])
                elif code_int >=4001 and code_int <=4051:
                    self.add_node("Q4001-Q4051", row['HCPC'])
                elif code_int >=4074 and code_int <=4082:
                    self.add_node("Q4074-Q4082", row['HCPC'])
                elif code_int >=4100 and code_int <=4286:
                    self.add_node("Q4100-Q4286", row['HCPC'])
                elif code_int >=5001 and code_int <=5010:
                    self.add_node("Q5001-Q5010", row['HCPC'])
                elif code_int >=5101 and code_int <=5101:
                    self.add_node("Q5101-Q5101", row['HCPC'])
                elif code_int >=5103 and code_int <=5111:
                    self.add_node("Q5103-Q5111", row['HCPC'])
                elif code_int >=5112 and code_int <=5131:
                    self.add_node("Q5112-Q5131", row['HCPC'])
                elif code_int >=9001 and code_int <=9004:
                    self.add_node("Q9001-Q9004", row['HCPC'])
                elif code_int >=9950 and code_int <=9983:
                    self.add_node("Q9950-Q9983", row['HCPC'])
                elif code_int >=9991 and code_int <=9992:
                    self.add_node("Q9991-Q9992", row['HCPC'])

            elif row['HCPC'][0] == 'R':
                if code_int >=70 and code_int<=76:
                    self.add_node("R0070-R0076", row['HCPC'])

            elif row['HCPC'][0] == 'S':
                if code_int >=12 and code_int <=197:
                    self.add_node("S0012-S0197", row['HCPC'])
                elif code_int >=199 and code_int <=400:
                    self.add_node("S0199-S0400", row['HCPC'])
                elif code_int >=500 and code_int <=596:
                    self.add_node("S0500-S0596", row['HCPC'])
                elif code_int >=601 and code_int <=622:
                    self.add_node("S0601-S0622", row['HCPC'])
                elif code_int >=630 and code_int <=3722:
                    self.add_node("S0630-S3722", row['HCPC'])
                elif code_int >=3800 and code_int <=3870:
                    self.add_node("S3800-S3870", row['HCPC'])
                elif code_int >=3900 and code_int <=3904:
                    self.add_node("S3900-S3904", row['HCPC'])
                elif code_int >=4005 and code_int <=4989:
                    self.add_node("S4005-S4989", row['HCPC'])
                elif code_int >=4990 and code_int <=5014:
                    self.add_node("S4990-S5014", row['HCPC'])
                elif code_int >=5035 and code_int <=5199:
                    self.add_node("S5035-S5199", row['HCPC'])
                elif code_int >=5497 and code_int <=5523:
                    self.add_node("S5497-S5523", row['HCPC'])
                elif code_int >=5550 and code_int <=5571:
                    self.add_node("S5550-S5571", row['HCPC'])
                elif code_int >=8030 and code_int <=8092:
                    self.add_node("S8030-S8092", row['HCPC'])
                elif code_int >=8096 and code_int <=8210:
                    self.add_node("S8096-S8210", row['HCPC'])
                elif code_int >=8265 and code_int <=9152:
                    self.add_node("S8265-S9152", row['HCPC'])
                elif code_int >=9208 and code_int <=9214:
                    self.add_node("S9208-S9214", row['HCPC'])
                elif code_int >=9325 and code_int <=9379:
                    self.add_node("S9325-S9379", row['HCPC'])
                elif code_int >=9381 and code_int <=9485:
                    self.add_node("S9381-S9485", row['HCPC'])
                elif code_int >=9490 and code_int <=9810:
                    self.add_node("S9490-S9810", row['HCPC'])
                elif code_int >=9900 and code_int <=9999:
                    self.add_node("S9900-S9999", row['HCPC'])

            elif row['HCPC'][0] == 'T':
                if code_int >=1000 and code_int <=1005:
                    self.add_node("T1000-T1005", row['HCPC'])
                elif code_int >=1006 and code_int <=1012:
                    self.add_node("T1006-T1012", row['HCPC'])
                elif code_int >=1013 and code_int <=1018:
                    self.add_node("T1013-T1018", row['HCPC'])
                elif code_int >=1019 and code_int <=1022:
                    self.add_node("T1019-T1022", row['HCPC'])
                elif code_int >=1023 and code_int <=1029:
                    self.add_node("T1023-T1029", row['HCPC'])
                elif code_int >=1030 and code_int <=1031:
                    self.add_node("T1030-T1031", row['HCPC'])
                elif code_int >=1032 and code_int <=1033:
                    self.add_node("T1032-T1033", row['HCPC'])
                elif code_int >=1040 and code_int <=1041:
                    self.add_node("T1040-T1041", row['HCPC'])
                elif code_int >=1502 and code_int <=1999:
                    self.add_node("T1502-T1999", row['HCPC'])
                elif code_int >=2001 and code_int <=2007:
                    self.add_node("T2001-T2007", row['HCPC'])
                elif code_int >=2010 and code_int <=2011:
                    self.add_node("T2010-T2011", row['HCPC'])
                elif code_int >=2012 and code_int <=2041:
                    self.add_node("T2012-T2041", row['HCPC'])
                elif code_int >=2042 and code_int <=2046:
                    self.add_node("T2042-T2046", row['HCPC'])
                elif code_int >=2047 and code_int <=2047:
                    self.add_node("T2047-T2047", row['HCPC'])
                elif code_int >=2048 and code_int <=2048:
                    self.add_node("T2048-T2048", row['HCPC'])
                elif code_int >=2049 and code_int <=2049:
                    self.add_node("T2049-T2049", row['HCPC'])
                elif code_int >=2050 and code_int <=2051:
                    self.add_node("T2050-T2051", row['HCPC'])
                elif code_int >=2101 and code_int <=2101:
                    self.add_node("T2101-T2101", row['HCPC'])
                elif code_int >=4521 and code_int <=4545:
                    self.add_node("T4521-T4545", row['HCPC'])
                elif code_int >=5001 and code_int <=5999:
                    self.add_node("T5001-T5999", row['HCPC'])

            elif row['HCPC'][0] == 'U':
                if code_int >=1 and code_int<=5:
                    self.add_node("U0001-U0005", row['HCPC'])

            elif row['HCPC'][0] == 'V':
                if code_int >=2020 and code_int <=2025:
                    self.add_node("V2020-V2025", row['HCPC'])
                elif code_int >=2100 and code_int <=2199:
                    self.add_node("V2100-V2199", row['HCPC'])
                elif code_int >=2200 and code_int <=2299:
                    self.add_node("V2200-V2299", row['HCPC'])
                elif code_int >=2300 and code_int <=2399:
                    self.add_node("V2300-V2399", row['HCPC'])
                elif code_int >=2410 and code_int <=2499:
                    self.add_node("V2410-V2499", row['HCPC'])
                elif code_int >=2500 and code_int <=2599:
                    self.add_node("V2500-V2599", row['HCPC'])
                elif code_int >=2600 and code_int <=2615:
                    self.add_node("V2600-V2615", row['HCPC'])
                elif code_int >=2623 and code_int <=2629:
                    self.add_node("V2623-V2629", row['HCPC'])
                elif code_int >=2630 and code_int <=2632:
                    self.add_node("V2630-V2632", row['HCPC'])
                elif code_int >=2700 and code_int <=2799:
                    self.add_node("V2700-V2799", row['HCPC'])
                elif code_int >=5008 and code_int <=5020:
                    self.add_node("V5008-V5020", row['HCPC'])
                elif code_int >=5030 and code_int <=5060:
                    self.add_node("V5030-V5060", row['HCPC'])
                elif code_int >=5070 and code_int <=5110:
                    self.add_node("V5070-V5110", row['HCPC'])
                elif code_int >=5120 and code_int <=5267:
                    self.add_node("V5120-V5267", row['HCPC'])
                elif code_int >=5268 and code_int <=5290:
                    self.add_node("V5268-V5290", row['HCPC'])
                elif code_int >=5298 and code_int <=5299:
                    self.add_node("V5298-V5299", row['HCPC'])
                elif code_int >=5336 and code_int <=5364:
                    self.add_node("V5336-V5364", row['HCPC'])



if __name__ == "__main__":
    hcpcs = Hcpcs()
    # print(hcpcd.get_descendants('M1003-M1070'))
    # all_codes = hcpcs.get_all_codes()
    # print(len(all_codes))
    # leaves = []
    # for c in all_codes:
    #     print(c)
        # if hcpcs.is_leaf(c) == True:
            # leaves.append(c)
            # print(c)
        # else:
            # print('no')
    # leaves
