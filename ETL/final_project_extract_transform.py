import pandas as pd

def extract_dataset(path_dd, path_gdp):
    
    df_disease = pd.read_csv(path_dd)
    df_gdp = pd.read_csv(path_gdp)
    
    return df_disease, df_gdp

def transform_dataset(df_disease, df_gdp):
    
    df_disease = df_disease.query("2009 < Year < 2023")
    df_disease = df_disease.drop(columns=["Availability of Vaccines/Treatment", "Improvement in 5 Years (%)", "Disease Category", "DALYs", "Urbanization Rate (%)"])
    df_disease = df_disease.rename(columns={"Country":"country", "Year":"year", "Disease Name":"disease_name", 
                                          "Prevalence Rate (%)":"prv_rate", "Incidence Rate (%)":"incd_rate", 
                                          "Mortality Rate (%)":"mortality_rate", "Age Group":"age_group", "Gender":"gender", 
                                          "Population Affected":"ppl_affected", "Healthcare Access (%)":"hlth_access", 
                                          "Doctors per 1000":"doctors_per_1000", "Hospital Beds per 1000":"hospital_beds_per_1000", 
                                          "Treatment Type": "trtmt_type", "Average Treatment Cost (USD)":"avg_trtmt_cost",  
                                          "Recovery Rate (%)":"rcvr_rate", "Education Index":"edc_index"})
    
    df_gdp = df_gdp.rename(columns={"Entity":"country", "Year":"year"})
    df_gdp = df_gdp.drop(columns=["900793-annotations", "Code"])
    df_gdp = df_gdp.query("year > 2009")
    
    merged_df = df_disease.merge(df_gdp, on=["country", "year"], how="inner")

    temp_df = merged_df.groupby(["country", 'trtmt_type', 'disease_name', 'gender', 'year', 'age_group'])["ppl_affected"].max().reset_index()
    final_df = merged_df.merge(temp_df, on=["country", 'trtmt_type', 'disease_name', 'gender', 'year', 'age_group', 'ppl_affected'])
 
    return final_df
    
df_disease, df_gdp = extract_dataset("/opt/airflow/Datasets/Global Health Statistics.csv", "/opt/airflow/Datasets/gdp-per-capita-maddison-project-database.csv")
final_df = transform_dataset(df_disease, df_gdp)
final_df.to_csv("/opt/airflow/Datasets/data_formated.csv")


    