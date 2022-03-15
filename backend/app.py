from flask import Flask, request
import pandas as pd

app = Flask(__name__)

@app.route('/api/load')
def load():
    return 'hello'

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # f.save(secure_filename(f.filename))
        return 'file uploaded successfully'
    else:
        return 'get request'

def isNullAny(df):
    return df.isnull().any()

def isNullColumn(columnName, df):
    return df[columnName].isnull()

def removeNullsFromDF(df):
    return df.dropna()

if __name__ == "__main__":
    app.run()         

