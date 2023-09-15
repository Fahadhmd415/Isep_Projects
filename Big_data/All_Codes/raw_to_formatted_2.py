
import os
from datetime import date
from pyspark.sql import SparkSession

HOME = '/home/fahadhmd/airflow/dags'
DATALAKE_ROOT_FOLDER = HOME + "/datalake/"

current_day = date.today().strftime("%Y%m%d")
file_name = "title.ratings.tsv.gz"


def raw_to_formatted_2():
    spark = SparkSession.builder.appName("TSVtoParquet").getOrCreate()

    RAW_FOLDER = DATALAKE_ROOT_FOLDER + "raw/imdb/" + current_day + "/" + file_name
    FORMATTED_FOLDER = DATALAKE_ROOT_FOLDER + "formatted/Ratings/" + current_day + "/"

    if not os.path.exists(FORMATTED_FOLDER):
        os.makedirs(FORMATTED_FOLDER)

    # Read TSV data using Spark
    df = spark.read.option("header", True).option("delimiter", "\t").csv(RAW_FOLDER)

    # Write data as Parquet with Snappy compression
    parquet_file_name = file_name.replace(".tsv.gz", ".snappy.parquet")
    df.write.format("parquet").option("compression", "snappy").save(FORMATTED_FOLDER + parquet_file_name)








