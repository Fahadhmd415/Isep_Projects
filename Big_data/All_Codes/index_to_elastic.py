
import pandas as pd
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from datetime import date

HOME = '/home/fahadhmd/airflow/dags'
DATALAKE_ROOT_FOLDER = HOME + "/datalake/"
current_day = date.today().strftime("%Y%m%d")

USAGE_FOLDER1 = DATALAKE_ROOT_FOLDER + "usage/averageRating_year/" + current_day + "/"
USAGE_FOLDER2 = DATALAKE_ROOT_FOLDER + "usage/numVotes_movies/" + current_day + "/"


"""
df = (
    pd.read_parquet(USAGE_FOLDER1 + "res.snappy.parquet")
    .dropna()
    .reset_index()
)
print(df)
print(list(df))

df1 = (
    pd.read_parquet(USAGE_FOLDER2 + "res.snappy.parquet")
    .dropna()
    .reset_index()
)
print(df1)
print(list(df1))
"""

def index_to_elastic():
    client = Elasticsearch(hosts=["http://localhost:9200"])

    """
    settings = {
        "settings" : {
            "number_of_shards" : 1,
            "number_of_replicas" : 0
        },
        "mappings" : {
            "properties": {
                "Number" : {"type":"integer"},
                "Year" : {"type":"integer"},
                "Average_rating" : {"type" : "float"},
                }
        }
    }
    
    client.indices.create(index="movies",body=settings)
    
    settings1 = {
        "settings" : {
            "number_of_shards" : 1,
            "number_of_replicas" : 0
        },
        "mappings" : {
            "properties": {
                "Number" : {"type":"integer"},
                "Year" : {"type":"integer"},
                "Average_rating" : {"type" : "float"},
                "Votes" : {"type" : "integer"},
                "Title" : {"type" : "text"},
                }
        }
    }
    
    client.indices.create(index="moviesvotes",body=settings1)
    
    bulk_data = []
    for i,row in df.iterrows():
        bulk_data.append(
            {
                "_index":"movies",
                "id":1,
                "_source":{
                    "Number" : row["index"],
                    "Year" : row["year"],
                    "Average_rating" : row["average_rating"]
                }
            }
        )
    
    bulk(client, bulk_data)
    
    bulk_data1 = []
    for i,row in df1.iterrows():
        bulk_data1.append(
            {
                "_index":"moviesvotes",
                "id":1,
                "_source":{
                    "Number" : row["index"],
                    "Year" : row["year"],
                    "Average_rating" : row["rating"],
                    "Votes" : row["numVotes"],
                    "Title" : row["title"],
                }
            }
        )
    
    
    
    bulk(client, bulk_data1)
    
    """














