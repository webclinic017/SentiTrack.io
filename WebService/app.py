from flask import Flask
from flask import render_template
import os
import json
import pytz
import pandas as pd
import plotly.graph_objects as go
import pymysql

app = Flask(__name__, template_folder='templates')

@app.route("/performance")
def getPerformance():
    with open("config.json") as f:
        config = json.load(f)

    db = pymysql.connect(host = config['host'], 
                         user = config['user'], 
                         password = config['password'], 
                         database = config['database'])
    cursor = db.cursor()
    cursor.execute('SELECT * FROM WSB')
    table_rows = cursor.fetchall()
    df = pd.DataFrame(table_rows)
    df.columns = ['Time', 'Sentiment', 'Market']
    db.close()

    #compute pct accuracy
    df['pct_chg'] = df['Market'].pct_change().shift(-1)
    correct = len(df[((df['pct_chg'] > 0) & (df['Sentiment'] > 0)) | ((df['pct_chg'] < 0) & (df['Sentiment'] < 0))])
    total = len(df[df['pct_chg'] != 0])
    pct_correct = round(correct/total, 2)

    #compute all time returns 
    df['pct_chg'] = df['pct_chg'] + 1
    returns = df['pct_chg'].prod()
    if returns > 1:
        pct_returns = round((returns - 1) * 100, 2)
    elif returns < 1:
        pct_returns = round((1 - returns) * -100, 2)
    return json.dumps({"accuracy": pct_correct, "returns": pct_returns})


@app.route("/data")
def getData():
    with open("config.json") as f:
        config = json.load(f)
    db = pymysql.connect(host = config['host'], 
                         user = config['user'], 
                         password = config['password'], 
                         database = config['database'])
    cursor = db.cursor()
    cursor.execute('SELECT * FROM WSB')
    table_rows = cursor.fetchall()
    db.close()
    
    df = pd.DataFrame(table_rows)
    df.columns = ['Time', 'Sentiment', 'Market']
    eastern = pytz.timezone('US/Eastern')
    df['Time'] = df['Time'].dt.tz_localize(pytz.utc).dt.tz_convert(eastern).astype(str)
    #df.set_index('Time', inplace=True)
    result = df.to_dict(orient='list')
    return json.dumps(result)

@app.route("/mentions")
def getMentions():
    with open("config.json") as f:
        config = json.load(f)
    db = pymysql.connect(host = config['host'], 
                         user = config['user'], 
                         password = config['password'], 
                         database = config['database'])
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM MENTIONS ORDER BY LogTime DESC LIMIT 1')
    table_row = cursor.fetchone()
    table_row['Logtime'] = table_row['Logtime'].strftime("%m/%d/%Y, %H:%M:%S")
    db.close()
    return json.dumps(table_row)

@app.route("/")
def index():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(debug=True)