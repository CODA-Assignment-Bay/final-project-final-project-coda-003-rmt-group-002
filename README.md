# Global Disease Statistic

## Final Project's Presentation Link
https://www.canva.com/design/DAGfne1kSo8/cPyEMq0U8seNPEUH3KTmHQ/edit?utm_content=DAGfne1kSo8&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

##**Link Looker **
https://lookerstudio.google.com/reporting/b59af51c-6251-40fc-8857-4559e907130d

## Dataset links

GDP per capita: https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database?tab=table&time=2000..latest

Global Health Statistic: https://www.kaggle.com/code/kirixaki/global-health-statistics-analysis

## Data Pipeline Architecture

Pipeline data berfungsi untuk melakukan otomasi proses pengambilan data, transform data, load data ke database, dan upload data ke spreadsheet.

## Step by step To Build The Pipeline

### 1. Extract Dataset Yang Digunakan

Cari dataset yang akan digunakan untuk dimasukkan ke dalam pipeline, bisa berupa dari API, file csv, dan lain-lain. Tapi untuk projek ini, kami menggunakan file csv.
Selanjutnya buat script python seperti pada file final_project_extract_transform.py yang ada di folder ETL. Buat fungsi untuk mengekstrak dataset.

### 2. Lakukan Explorasi Ringan Pada Dataset

Cek isi data, tipe-tipe data, dll yang sekiranya diperlukan dan lakukan data cleaning ringan agar dataset dapat dianalisis.
Kalian juga dapat menggunakan GreatExpectations untuk melakukan validasi data sesuai kebutuhan, seperti pada file fp_gx.ipynb

### 3. Transform Dataset

Transform data sesuai kebutuhan, seperti mengubah tipe data, mengubah nama kolom menjadi snake case, ataupun menggabungkan dataset.
Contoh pembuatan fungsi untuk transform data ada pada file final_project_extract_transform.py.

### 4. Load Dataset

Setelah dataset sudah siap diload, buat fungsi untuk melakukan load dataset ke RDBMS atau database lain.
Pada projek ini, kami menggunakan mongoDB sebagai database kami.

#### How to Setup MongoDB

1. Buat akun mongoDB di website: https://cloud.mongodb.com/v2
2. Setelah buat akun, pergi ke tab cluster di website tersebut, lalu pilih buat cluster baru dengan konfigurasi gratis dan gunakan google cloud services.
3. Setelah itu, pergi ke tab cluster lagi, dan pilih connect -> compass. Di bagian ini akan muncul link yang akan digunakan untuk membuat koneksi ke mongoDB yang nantinya akan digunakan dalam file python/ipynb.
4. Pindah ke tab Quickstart dan scroll ke bawah hingga menemukan bagian untuk memasukkan IP Address. masukan entry baru dengan IP 0.0.0.0 agar semua IP address bisa mengakses database tersebut.
5. Di bagian atas tab Quickstart, buatlah username baru dan password, yang nantinya digunakan untuk mengisi link yang mengkoneksikan database.
6. Download mongoDB compass: https://www.mongodb.com/try/download/compass untuk melakukan monitoring database kalian. Masukkan link koneksi cluster kalian saat ingin membuat databse di mongoDB compass.
7. Ikuti script di file final_project_extract_load.py dan ubah link pengkoneksian ke mongoDB, nama database, dan nama collectionnya. Contoh:
   ```py
    client = MongoClient("mongodb+srv://admin:admin@adams-playground4.s8xqk.mongodb.net/?serverSelectionTimeoutMS=5000")
    database = client["final_project_CODA_003_group_002"]
    my_collection = database["Data-coll"]
   ```

### 5. Membuat Pipeline

Pipeline pada projek ini berfungsi untuk melakukan penjadwalan sehingga proses ETL akan dilakukan secara otomatis sesuai yang sudah dijadwalkan.
Simpan semua file extract, transform, load, dan load mongo to sheet yang sudah kalian buat ke dalam folder dag airflow yang ada di pc/laptop kalian.
Setelah itu, buat file airflow DAG yang berisikan flow kerja dari pipeline yang kalian inginkan, seperti di file Airflowfinalproject_pipeline.py. Contoh:
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

Ketika data sudah berhasil diload ke mongo, selanjutnya kita akan membuat datamart yang dapat diakses untuk proses analisis secara otomatis.
Salah satu caranya adalah mengupload datanya ke spreadsheet, menggunakan spreadsheet API.

#### How to Setup Spreadsheet

1. Buka link: https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com dan klik enable.
2. Setelah itu, klik manage untuk mengatur API.
3. Pilih tab credentials, dan buat service account.
4. Setelah itu, copy email dari service account yang sudah dibuat.
5. Buat spreadsheet baru, dan share access ke email yang sudah dibuat sebelumnya.
6. Pergi ke tab credentials lagi, dan klik email yang sudah dibuat.
7. Selanjutnya pergi ke tab keys, dan pilih add key dan create new key, setelah itu download key tersebut.
8. Buat file python untuk mengupload data mongoDB ke spreadsheet, seperti file mongo_to_sheet.py.
9. Buat koneksi dengan mongoDB dan spreadsheet, Contoh:

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

Setelah melakukan setup spreadsheet, ikuti fungsi-fungsi yang ada di file mongo_to_sheet.py untuk melakukan upload ke spreadsheet.



