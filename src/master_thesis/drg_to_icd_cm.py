import pandas as pd
from master_thesis.simple_icd_10_cm import SimpleIcd10Cm

class Drg_to_icd_cm(SimpleIcd10Cm):
    @staticmethod
    def drg_to_icd():

        data = pd.read_csv('./src/master_thesis/taxonomies/raw_drg_data.csv')
        df1 = pd.read_csv("data/drgcodes.csv")
        df2 = df1.loc[df1["drg_type"] == 'HCFA']

        data.drop('description_detailed', axis=1, inplace=True)

        data['identifier_detailed'] = data['identifier_detailed'].str[:3]

        aggregated_data = data.groupby(['identifier', 'identifier_detailed']).size().reset_index(name='count')

        counts = aggregated_data.groupby('identifier')['identifier_detailed'].nunique()

        filtered_identifiers = counts[counts <= 20].index
        final_data = aggregated_data[aggregated_data['identifier'].isin(filtered_identifiers)]

        final_data.rename(columns={'identifier': 'drg_code'}, inplace=True)

        merged_data = pd.merge(df2,final_data, on='drg_code', how='inner')
        merged_data['seq_num'] = merged_data.groupby('hadm_id').cumcount() + 1

        merged_data.rename(columns={'identifier_detailed': 'icd_code'}, inplace=True)
        merged_data.drop('count', axis=1, inplace=True)

        merged_data.to_csv('data/drg_to_icd.csv',index=False)


if __name__ == "__main__":
    Drg_to_icd_cm.drg_to_icd()
    