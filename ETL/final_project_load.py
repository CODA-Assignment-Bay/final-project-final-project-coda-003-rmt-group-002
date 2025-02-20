from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, BooleanType

def load_data_to_mongo(file_path):
    
    data = pd.read_csv(file_path)
    document_list = data.to_dict(orient='records')
    doc_len = len(document_list)

    
    for x in range(1, len(document_list)+1, 10000):
        if (x + 10000) <= (doc_len+1):
            tmp_doc_list = document_list[x:x+10000]
            client['final_project_CODA_003_group_002']['Data-coll'].insert_many(tmp_doc_list)
        elif (x + 10000) > (doc_len+1):
            tmp_doc_list = document_list[x:(doc_len+1)]
            client['final_project_CODA_003_group_002']['Data-coll'].insert_many(tmp_doc_list)
    return 
    # data_disease = pd.read_csv(file_path_dd)
    # data_gdp = pd.read_csv(file_path_gdp)
    
    # document_list_dd = data_disease.to_dict(orient='records')
    # document_list_gdp = data_gdp.to_dict(orient='records')
    # doc_len = len(document_list_dd)
    
    # for x in range(1, len(document_list_dd)+1, 10000):
    #     if (x + 10000) <= (doc_len+1):
    #         tmp_doc_list1 = document_list_dd[x:x+10000]
    #         tmp_doc_list2 = document_list_gdp[x:x+10000]
    #         client['final_project_CODA_003_group_002']['disease-coll'].insert_many(tmp_doc_list1)
    #         client['final_project_CODA_003_group_002']['gdp-coll'].insert_many(tmp_doc_list2)
    #     elif (x + 10000) > (doc_len+1):
    #         # tmp_doc_list = document_list[x:(doc_len+1)]
    #         tmp_doc_list1 = document_list_dd[x:(doc_len+1)]
    #         tmp_doc_list2 = document_list_gdp[x:(doc_len+1)]
    #         client['final_project_CODA_003_group_002']['disease-coll'].insert_many(tmp_doc_list1)
    #         client['final_project_CODA_003_group_002']['gdp-coll'].insert_many(tmp_doc_list2)
    # return
    
client = MongoClient("mongodb+srv://admin:admin@adams-playground4.s8xqk.mongodb.net/?serverSelectionTimeoutMS=5000")
database = client["final_project_CODA_003_group_002"]
my_collection = database["Data-coll"]
total_doc = my_collection.count_documents({})

if total_doc == 0:
    load_data_to_mongo("/opt/airflow/Datasets/data_formated.csv")
else:
    print("Data is loaded")


