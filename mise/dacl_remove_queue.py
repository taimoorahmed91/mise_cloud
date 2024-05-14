import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

insertid = sys.argv[1]



connection = mysql.connector.connect(host='127.0.0.1',
                                     database='mise',
                                     user='root',
                                     password='C1sc0123@')




cursor = connection.cursor(dictionary=True)
sql_update_query = """Update dacl set queue = 'no' where id = %s"""
input_data = (insertid, )
cursor.execute(sql_update_query, input_data)
connection.commit()
