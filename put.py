import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("CONN_URL")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

with open('data.json') as data:
    data_str = json.dumps(json.load(data))

req = requests.put(url, data=data_str, headers=headers)

#Debug prints
#print(req)
#print(req.json())
