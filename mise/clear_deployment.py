import urllib3
import requests
import sys
import json
import mysql.connector
import contextlib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

connection = mysql.connector.connect(host='database',
                                     database='mise',
                                     user='root',
                                     password='C1sc0123@')




cursor = connection.cursor(dictionary=True)
sql_update_query = """Update deployments set marked = 'no'"""
cursor.execute(sql_update_query, )
connection.commit()
