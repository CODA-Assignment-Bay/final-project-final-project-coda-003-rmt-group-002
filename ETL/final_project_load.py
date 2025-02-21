from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, BooleanType

# Fungsi untuk melakukan load ke mongoDB
def load_data_to_mongo(file_path):
    
    data = pd.read_csv(file_path)
    document_list = data.to_dict(orient='records')
    doc_len = len(document_list)

    # Fungsi untuk melakukan load data ke mongoDB per 10000 document
    for x in range(1, len(document_list)+1, 10000):
        if (x + 10000) <= (doc_len+1):
            tmp_doc_list = document_list[x:x+10000]
            client['final_project_CODA_003_group_002']['Data-coll'].insert_many(tmp_doc_list)
        elif (x + 10000) > (doc_len+1):
            tmp_doc_list = document_list[x:(doc_len+1)]
            client['final_project_CODA_003_group_002']['Data-coll'].insert_many(tmp_doc_list)
    return 

# Membuat koneksi ke mongoDB
client = MongoClient("mongodb+srv://admin:admin@adams-playground4.s8xqk.mongodb.net/?serverSelectionTimeoutMS=5000")
database = client["final_project_CODA_003_group_002"]
my_collection = database["Data-coll"]

total_doc = my_collection.count_documents({})

if total_doc == 0:
    # Sesuaikan file_path 
    load_data_to_mongo("/opt/airflow/Datasets/data_formated.csv")
else:
    print("Data is loaded")


