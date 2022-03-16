from flask import Flask, request, abort, send_from_directory
import pandas as pd
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['UPLOAD_PATH'] = '../csv'

@app.route('/api/load')
def load():
    return 'hello'

@app.route('/uploader', methods = ['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Not a csv", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return "Saved", 204
    return "No file attached", 400

@app.route("/downloader/<file_name>")
def get_image(file_name):
    try:
        return send_from_directory(directory=app.config["UPLOAD_PATH"], path=file_name)
    except FileNotFoundError:
        abort(404)        
        
@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

def isNullAny(df):
    return df.isnull().any()

def isNullColumn(columnName, df):
    return df[columnName].isnull()

def removeNullsFromDF(df):
    return df.dropna()

if __name__ == "__main__":
    app.run()         

