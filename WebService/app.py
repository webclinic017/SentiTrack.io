from flask import Flask
from flask import render_template
import os
import json
from config import db
import pytz
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__, template_folder='templates')

@app.route("/performance")
def getPerformance():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM WSB')
    table_rows = cursor.fetchall()
    df = pd.DataFrame(table_rows)
    df.columns = ['Time', 'Sentiment', 'Market']

    #compute pct accuracy
    df['pct_chg'] = df['Market'].pct_change().shift(-1)
    correct = len(df[((df['pct_chg'] > 0) & (df['Sentiment'] > 0)) | ((df['pct_chg'] < 0) & (df['Sentiment'] < 0))])
    total = len(df[df['pct_chg'] != 0])
    pct_correct = round(correct/total, 2)

    #compute all time returns 
    df['pct_chg'] = df['pct_chg'] + 1
    returns = round(df['pct_chg'].prod(),3)
    return json.dumps({"accuracy": pct_correct, "returns": returns})


@app.route("/data")
def getData():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM WSB')
    table_rows = cursor.fetchall()
    df = pd.DataFrame(table_rows)
    df.columns = ['Time', 'Sentiment', 'Market']
    eastern = pytz.timezone('US/Eastern')
    df['Time'] = df['Time'].dt.tz_localize(pytz.utc).dt.tz_convert(eastern).astype(str)
    #df.set_index('Time', inplace=True)
    result = df.to_dict(orient='list')
    return json.dumps(result)

@app.route("/")
def index():
    return render_template('main.html')