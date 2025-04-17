import requests
import pymssql
import datetime
import re
import json
import os
from dotenv import load_dotenv

load_dotenv()
#---
SERVER = os.getenv("SQL_SERV")
DB = os.getenv("SQL_DB")
USER = os.getenv("SQL_USER")
PASS = os.getenv("SQL_PASS")
#---

SQL_QUERY = """
SELECT * FROM Order_Table
"""

def fetchOrders():
    orders_list = ""
    conn = pymssql.connect(server=SERVER, user=USER, password=PASS, database=DB, as_dict=True)
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    entries = cursor.fetchall()

    track = 1
    for ent in entries:
        line = str(ent)
        result = re.search('\'order_time\': (.*), \'order_status\'', str(ent))
        subsect = "\"" + result.group(1) + "\""
        line = line.replace(result.group(1), subsect)

        if (track != cursor.rowcount):
            orders_list = orders_list + (line + ",\n            ")
        else:
            orders_list = orders_list + line
        track += 1

    orders_list = orders_list.replace('\'', '\"')
    cursor.close()
    conn.close()
    return orders_list

def updateJson():
    #maintain dyn_list
    fp = open("data.json", "r")
    result = re.search('\"dyn_list\": \\[\n(.*)\"orders\"', fp.read(), flags=re.DOTALL)
    dyn_list = result.group(1)
    fp.close()

    #get updated list of orders
    orders_list = fetchOrders()

    f = open("data2.json", "w")
    args = (dyn_list, orders_list)
    f.write("""
{{
    "data": {{
        "dyn_list": [
{0}"orders": [
            {1}
        ],
        "cmds": [
            {{
                
            }}
        ]
    }}
}}
    """.format(*args))
    f.close()


url = os.getenv("CONN_URL")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
req = requests.get(url, headers=headers)

print(req)
print(req.json())

obj = req.json()
print("\n")
print(obj['data']['cmds'])

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
    vals = (order_id, order_type, datetime.datetime.now(), "pending", vendor) #fix datetime mismatch w/ db

    cursor.execute(ADD_QUERY, vals)
    

    cursor.execute(SQL_QUERY)
    entries = cursor.fetchall()
    for ent in entries:
        print(ent)

    conn.commit() #persist data

    cursor.close()
    conn.close()

updateJson()