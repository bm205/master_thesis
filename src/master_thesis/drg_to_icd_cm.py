import pandas as pd
from master_thesis.simple_icd_10_cm import SimpleIcd10Cm

class Drg_to_icd_cm(SimpleIcd10Cm):
    @staticmethod
    def drg_to_icd():

        df = pd.read_csv("./src/master_thesis/taxonomies/raw_drg_data.csv")
        df1 = pd.read_csv("data/drgcodes.csv", dtype=str)
        df2 = df1.loc[df1["drg_type"] == 'HCFA']

        data = {'drg_code': [], 'icd_code':[],'seq_num':[]}

        dataframe = pd.DataFrame(data)

        previous_row = 'E08'
        previous_drg = '008'
        counter_icd = 0
        counter_drg = 1
        to_remove = []

        for _, row in df.iterrows():
            icd_code = row['identifier_detailed'][0]+row['identifier_detailed'][1]+row['identifier_detailed'][2]

            if row['identifier'] == previous_drg:
                if icd_code == previous_row:
                    counter_icd = counter_icd + 1
                else:
                    drg_code=row['identifier']
                    dataframe.loc[len(dataframe.index)] = [drg_code, previous_row, counter_drg]
                    counter_drg = counter_drg + 1
                    counter_icd = 1
                    
            else:
                if counter_drg > 20:
                    to_remove.append(previous_drg)
                drg_code=row['identifier']
                dataframe.loc[len(dataframe.index)] = [previous_drg, previous_row, counter_drg]
                counter_icd = 1
                counter_drg = 1
            
            if row['identifier'] == 'identifier':
                break
            
            previous_row = icd_code
            previous_drg = row['identifier']

        dataframe_final = dataframe
        for i in to_remove:
            dataframe_final = dataframe_final.loc[dataframe["drg_code"] != i]

        df3 = df2
        for i in to_remove:
            df3 = df3.loc[df2["drg_code"] != i]

        join = pd.merge(df3,dataframe_final,on='drg_code',how='inner')

        join.to_csv('data/drg_to_icd.csv')

if __name__ == "__main__":
    Drg_to_icd_cm.drg_to_icd()
    