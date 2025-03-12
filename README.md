# Global Disease Statistic

This project analyzes and explores the relationship between disease prevalence, healthcare infrastructure, and economic conditions across various countries. The goal is to provide insights into how income levels, education, and access to healthcare services influence disease severity and mortality rates.

## Final Project's Presentation Link
https://www.canva.com/design/DAGfne1kSo8/cPyEMq0U8seNPEUH3KTmHQ/edit?utm_content=DAGfne1kSo8&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## Dashboard Link
https://lookerstudio.google.com/reporting/b59af51c-6251-40fc-8857-4559e907130d

## Dataset links

GDP per capita: https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database?tab=table&time=2000..latest

Global Health Statistic: https://www.kaggle.com/code/kirixaki/global-health-statistics-analysis

## Tools

- Looker Studio
- Spreadsheet API
- MongoDB
- Apache Airflow
- Pandas
- Python

## Data Pipeline Architecture

The data pipeline automates the process of data extraction, transformation, loading into a database, and uploading to a spreadsheet.

## Step by step To Build The Pipeline

### 1. Extract the Dataset

Select the dataset to be included in the pipeline, which can be from APIs, CSV files, etc. For this project, we use CSV files.
Create a Python script as seen in final_project_extract_transform.py in the ETL folder. Develop a function to extract the dataset.

### 2. Perform Initial Data Exploration

Check the dataset’s content, data types, and perform basic cleaning to ensure analysis readiness. You can use Great Expectations for data validation, as demonstrated in fp_gx.ipynb.

### 3. Transform the Dataset

Transform the dataset as needed, such as changing data types, renaming columns to snake_case, or merging datasets. 
Example functions for data transformation can be found in final_project_extract_transform.py.

### 4. Load the Dataset

Once the dataset is ready, create functions to load it into an RDBMS or other databases. In this project, we use MongoDB.

#### How to Setup MongoDB

1. Create a MongoDB account at https://cloud.mongodb.com/v2
2. Go to the Clusters tab and create a new free cluster using Google Cloud services.
3. In the Clusters tab, select Connect → Compass. Copy the connection link for use in Python/IPython files.
4. Under the Quickstart tab, scroll down to enter an IP Address. Add 0.0.0.0 to allow all IPs to access the database.
5. At the top of the Quickstart tab, create a new username and password to connect to the database.
6. Download mongoDB compass: https://www.mongodb.com/try/download/compass to monitor your database.
7. Modify the connection script in final_project_extract_load.py with the correct MongoDB URI, database, and collection name. Example:
   ```py
    client = MongoClient("mongodb+srv://admin:admin@adams-playground4.s8xqk.mongodb.net/?serverSelectionTimeoutMS=5000")
    database = client["final_project_CODA_003_group_002"]
    my_collection = database["Data-coll"]
   ```

### 5. Creating the Data Pipeline

The pipeline schedules and automates the ETL process.
Store all extract, transform, and load scripts inside the dag airflow folder on your local machine.
Then, create an Airflow DAG file to define the pipeline workflow as seen in Airflowfinalproject_pipeline.py. Example:
```py
    # Sesuaikan semua parameter default_args dengan kebutuhan
    default_args = {
        'owner': 'adam',
        'start_date': dt.datetime(2024, 1, 11),
        'retries': 1,
        'retry_delay': dt.timedelta(minutes=10),
    }

    with DAG('load_fp_datas',
            default_args=default_args,
            schedule_interval='10-30/10 9 * * 6',
            catchup = False,
            ) as dag:

    # Sesuaikan task-task apa saja yang akan dilakukan serta path ke file yang digunakan

    get_FP_data = BashOperator(task_id='get_FP_data', bash_command='python /opt/airflow/ETL/final_project_extract_transform.py')

    load_FP_data = BashOperator(task_id='load_FP_data', bash_command='python /opt/airflow/ETL/final_project_load.py')

    load_to_sheet = BashOperator(task_id='load_to_sheet', bash_command='python /opt/airflow/ETL/mongo_to_sheet.py')

    get_FP_data >> load_FP_data >> load_to_sheet
```

### 6. Load to Spreadsheet

Once data is successfully loaded into MongoDB, create a data mart that can be accessed for automated analysis.
One way to do this is by uploading data to a Google Spreadsheet using the Google Sheets API.

#### How to Setup Spreadsheet

1. Open this link: https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com and enable it.
2. Click Manage to configure the API.
3. Navigate to the Credentials tab and create a new Service Account.
4. Copy the service account email.
5. Create a new Google Spreadsheet and share access with the copied email.
6. In the Credentials tab, click on the service account email.
7. Go to the Keys tab, select Add Key, and download the generated key file.
8. Create a Python script to upload MongoDB data to Google Sheets, as shown in mongo_to_sheet.py.
9. Establish connections to MongoDB and Google Sheets. Example:

   ```py
    # Membuat koneksi ke mongoDB
    client = MongoClient("mongodb+srv://admin:admin@adams-playground4.s8xqk.mongodb.net/?serverSelectionTimeoutMS=5000")
    database = client["final_project_CODA_003_group_002"]
    my_collection = database["Data-coll"]

    # Membuat koneksi ke Google Sheets

    # Sesuaikan service account filenya dengan file key yang sudah didownload dan juga spreadsheet_idnya
    SERVICE_ACCOUNT_FILE = "/opt/airflow/ETL/final-project-havktiv8-58b34f290147.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # Spreadsheet id adalah kode yang ada setelah "/d/" dari https://docs.google.com/spreadsheets/d/1ihkKi3KTsZFcaLXnHiLhEQlMjI-JW5y71s-8ijmon14/
    SPREADSHEET_ID = "1H2-51X2KYwen_bns88SqfoYoadF_de8n_U-mK-zQPF8"
    RANGE_NAME = "raw_data!A:Z"
   ```

After setting up the Google Sheets API, follow the functions in mongo_to_sheet.py to upload the data to Google Sheets automatically.



