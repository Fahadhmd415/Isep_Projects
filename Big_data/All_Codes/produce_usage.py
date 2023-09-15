
import os
from pyspark.sql import SQLContext
from datetime import date

HOME = '/home/fahadhmd/airflow/dags'
DATALAKE_ROOT_FOLDER = HOME + "/datalake/"
current_day = date.today().strftime("%Y%m%d")

file_name1 = "extract.snappy.parquet"
file_name2 = "title.ratings.snappy.parquet"



def produce_usage():
   FORMATTED_FOLDER1 = DATALAKE_ROOT_FOLDER + "formatted/Moviedata/" + current_day + "/" + file_name1
   FORMATTED_FOLDER2 = DATALAKE_ROOT_FOLDER + "formatted/Ratings/" + current_day + "/" + file_name2

   USAGE_FOLDER1 = DATALAKE_ROOT_FOLDER + "usage/averageRating_year/" + current_day + "/"
   USAGE_FOLDER2 = DATALAKE_ROOT_FOLDER + "usage/numVotes_movies/" + current_day + "/"

   if not os.path.exists(USAGE_FOLDER1):
       os.makedirs(USAGE_FOLDER1)
   if not os.path.exists(USAGE_FOLDER2):
       os.makedirs(USAGE_FOLDER2)

   from pyspark import SparkContext

   sc = SparkContext(appName="CombineData")
   sqlContext = SQLContext(sc)
   df_data = sqlContext.read.parquet(FORMATTED_FOLDER2)
   df_data.registerTempTable("data")
   df_rating = sqlContext.read.parquet(FORMATTED_FOLDER1)
   df_rating.registerTempTable("ratings")

   # Check content of the DataFrame df_ratings:
   print(df_data.show())
   print(df_rating.show())

   averageRating_year = sqlContext.sql(" SELECT api2.year, "
 " AVG(api1.averageRating) AS average_rating "
 " FROM data AS api1 "
 " JOIN ratings AS api2 ON api1.tconst = api2.imdbid "
 " GROUP BY api2.year "
 " ORDER BY api2.year; " )


   numVotes_movies = sqlContext.sql(" SELECT api1.numVotes, "
    " api1.averageRating AS rating, "
    " api2.title, "
    " api2.year "                         
    " FROM data AS api1 "
    " JOIN ratings AS api2 ON api1.tconst = api2.imdbid "
    " WHERE api2.year > 2000 AND api1.averageRating > 8.0 "
   )


   # Check content of the DataFrame stats_df and save it:
   print(averageRating_year.show())
   averageRating_year.write.save(USAGE_FOLDER1 + "res.snappy.parquet", mode="overwrite")

   # Check content of the DataFrame top10_df  and save it:
   print(numVotes_movies.show())
   numVotes_movies.write.save(USAGE_FOLDER2 + "res.snappy.parquet", mode="overwrite")





