from flask import Flask
import pandas as pd

app = Flask(__name__)

@app.route('/api/load')
def load():
    return 'hello'

def isNullAny(df):
    return df.isnull().any()

def isNullColumn(columnName, df):
    return df[columnName].isnull()

def removeNullsFromDF(df):
    return df.dropna()

if __name__ == "__main__":
    app.run(host ='0.0.0.0')         

