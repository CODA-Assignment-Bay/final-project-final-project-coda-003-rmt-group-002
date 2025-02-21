import pymongo
import pandas as pd
import time
from pymongo import MongoClient
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Membuat koneksi ke mongoDB
client = MongoClient("mongodb+srv://admin:admin@adams-playground4.s8xqk.mongodb.net/?serverSelectionTimeoutMS=5000")
database = client["final_project_CODA_003_group_002"]
my_collection = database["Data-coll"]

# Membuat koneksi ke Google Sheets

# Sesuaikan keys dan juga spreadsheet_idnya
SERVICE_ACCOUNT_FILE = "/opt/airflow/ETL/final-project-havktiv8-58b34f290147.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = "1H2-51X2KYwen_bns88SqfoYoadF_de8n_U-mK-zQPF8"
RANGE_NAME = "raw_data!A:Z"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('sheets', 'v4', credentials=credentials)

# Fungsi untuk melakukan write ke spreadsheet
def write_to_spreadsheet(body):
    result = service.spreadsheets().values().update(
        spreadsheetId = SPREADSHEET_ID,
        range = RANGE_NAME,
        valueInputOption = "RAW",
        body=body
    ).execute()
    return result

# Fungsi untuk membersihkan spreadsheet
def clear_spreadsheet():
    service.spreadsheets().values().clear(
        spreadsheetId = SPREADSHEET_ID,
        range = RANGE_NAME
    ).execute()

# Fungsi untuk mengecek apakah sheet kosong
def is_sheet_empty():
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    
    values = result.get('values', [])
    return len(values) == 0

# Fungsi untuk melakukan append ke spreadsheet
def write_append_spreadsheet(body):
    append_request = service.spreadsheets().values().append(
        spreadsheetId = SPREADSHEET_ID,
        range = RANGE_NAME,
        valueInputOption = "RAW",
        insertDataOption = "INSERT_ROWS",
        body = body
    ).execute()

# Fungsi untuk mengambil data dari mongo
def get_datas_from_mongo():
    db_len = my_collection.count_documents({})
    doc_list = []
    
    # Batch sizenya bisa disesuaikan dengan kebutuhan
    for x in range(0, db_len, 10000):
        if (x + 10000) <= (db_len):
            doc_list += (list(my_collection.find().batch_size(10000)[x:x+10000]))
        elif (x + 10000) > (db_len):
            doc_list += (list(my_collection.find()[x:db_len]))
    return doc_list

# Fungsi untuk melakukan load ke sheet
def load_to_sheet():
    db_len = my_collection.count_documents({})
    print("Getting datas...")
    doc_list = get_datas_from_mongo()
    print("Datas loaded")
    dict_values =[]
    
    df = pd.DataFrame(doc_list)
    df = df.drop(columns=["_id", "Unnamed: 0"])
    
    print("inserting datas to sheet...")

    # Max rows dapat disesuaikan
    MAX_ROWS = 900000
    datas_to_sheet = df.iloc[0:int(df.shape[0]),:]
    body_coll = [datas_to_sheet.columns.tolist()]
    body_coll = {"values": body_coll}

    write_to_spreadsheet(body_coll)
        
    body = datas_to_sheet.values.tolist() 
    body = {"values": body}
    
    # Batch size dapat disesuaikan
    for x in range(0, int(df.shape[0]/5000)):
        x = x*5000
        print(x)
        datas_to_sheet = df.iloc[x:x+5000,:]
        
        # body = list(datas_to_sheet) 
        body = datas_to_sheet.values.tolist()
        body = {"values": body}
        
        result = write_append_spreadsheet(body)
        time.sleep(1)
                
    return

if is_sheet_empty():
    print("Loading data...")
    load_to_sheet()
else:
    print("Data already loaded")
