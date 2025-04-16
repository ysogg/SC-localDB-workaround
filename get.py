import requests
import pymssql
import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("CONN_URL")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
req = requests.get(url, headers=headers)

print(req)
print(req.json())

obj = req.json()
print("\n")
print(obj['data']['cmds'])


#---
SERVER = os.getenv("SQL_SERV")
DB = os.getenv("SQL_DB")
USER = os.getenv("SQL_USER")
PASS = os.getenv("SQL_PASS")

SQL_QUERY = """
SELECT * FROM Order_Table
"""
#---

numCmds = len(obj['data']['cmds'])
#Debug
if (numCmds > 0):
    print("got {0} cmd(s)".format(numCmds))

    conn = pymssql.connect(server=SERVER, user=USER, password=PASS, database=DB, as_dict=True)

    cursor = conn.cursor()
    
    #test vals
    order_id = 112
    order_type = "py_test"
    vendor = "py_vendor_test"

    ADD_QUERY = "INSERT INTO Order_Table (order_id, order_type, order_time, order_status, vendor) VALUES (%s, %s, %s, %s, %s)"
    vals = (order_id, order_type, datetime.datetime.now(), "pending", vendor)

    cursor.execute(ADD_QUERY, vals)
    

    cursor.execute(SQL_QUERY)
    entries = cursor.fetchall()
    for ent in entries:
        print(ent)

    conn.commit() #persist data

    cursor.close()
    conn.close()