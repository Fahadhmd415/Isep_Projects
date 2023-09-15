import os
from datetime import date

import requests

HOME = '/home/fahadhmd/airflow/dags'
DATALAKE_ROOT_FOLDER = HOME + "/datalake/"

def source_to_raw_1(**kwargs):
    current_day = date.today().strftime("%Y%m%d")

    url = "https://imdb-top-100-movies1.p.rapidapi.com/"

    headers = {
        "X-RapidAPI-Key": "b4c2b91fcemshec2addb6175f22ep122986jsn03535c95625d",
        "X-RapidAPI-Host": "imdb-top-100-movies1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    filename = 'extract.json'

    path =  DATALAKE_ROOT_FOLDER + "raw/rapidapi/" + current_day + "/"
    os.makedirs(path, exist_ok=True)
    with open(path + filename, 'w') as f:
        f.write(response.text)




