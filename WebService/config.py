import json
import pymysql

with open("config.json") as f:
        config = json.load(f)

db = pymysql.connect(host = config['host'], 
                         user = config['user'], 
                         password = config['password'], 
                         database = config['database'])



