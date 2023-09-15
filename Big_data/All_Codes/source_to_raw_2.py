
import os
from datetime import date

import requests

HOME = '/home/fahadhmd/airflow/dags'
DATALAKE_ROOT_FOLDER = HOME + "/datalake/"

def source_to_raw_2(**kwargs):
    current_day = date.today().strftime("%Y%m%d")

    url = 'https://datasets.imdbws.com/title.ratings.tsv.gz'


    path =  DATALAKE_ROOT_FOLDER + "raw/imdb/" + current_day + "/"
    os.makedirs(path, exist_ok=True)
    r = requests.get(url, allow_redirects=True)
    open(path + 'title.ratings.tsv.gz', 'wb').write(r.content)




