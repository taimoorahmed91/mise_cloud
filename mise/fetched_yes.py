import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

insertid = sys.argv[1]



connection = mysql.connector.connect(host='database',
                                     database='mise',
                                     user='root',
                                     password='C1sc0123@')




cursor = connection.cursor(dictionary=True)
sql_update_query = """Update deployments set fetched = 'yes' where id = %s"""
input_data = (insertid, )
cursor.execute(sql_update_query, input_data)
connection.commit()



cursor = connection.cursor(dictionary=True)
sql_update_query = """Update deployments set fetchedon = CURRENT_TIMESTAMP where id = %s"""
input_data = (insertid, )
cursor.execute(sql_update_query, input_data)
connection.commit()
