
import os
from datetime import date
from pyspark.sql import SparkSession

HOME = '/home/fahadhmd/airflow/dags'
DATALAKE_ROOT_FOLDER = HOME + "/datalake/"

current_day = date.today().strftime("%Y%m%d")
file_name = "extract.json"


def raw_to_formatted_1():
   spark = SparkSession.builder.appName("DataFormatting").getOrCreate()

   RAW_FOLDER = DATALAKE_ROOT_FOLDER + "raw/rapidapi/" + current_day + "/" + file_name
   FORMATTED_FOLDER = DATALAKE_ROOT_FOLDER + "formatted/Moviedata/" + current_day + "/"

   if not os.path.exists(FORMATTED_FOLDER):
      os.makedirs(FORMATTED_FOLDER)

   df = spark.read.json(RAW_FOLDER)
   parquet_file_name = file_name.replace(".json", ".snappy.parquet")
   df.write.format("parquet").option("compression", "snappy").save(FORMATTED_FOLDER + parquet_file_name)


