import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("CONN_URL")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
req = requests.get(url, headers=headers)

print(req)
print(req.json())
