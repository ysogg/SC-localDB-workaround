import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("CONN_URL")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
payload = open("data.json")
req = requests.post(url, data=payload, headers=headers)

print(req)
print(req.json())
