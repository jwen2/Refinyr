from flask import Flask, request, abort, send_from_directory
from io import StringIO
from werkzeug.wrappers import Response
from flask_cors import CORS
from os import walk, path, remove
import pandas_func
import datastore
import pandas as pd

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['UPLOAD_PATH'] = '../csv'
app.config['MAX_HEADER_ROWS'] = 1000

@app.before_request
def before_request():
    app.logger.debug('before_request')
    datastore.get_datastore()

@app.after_request
def after_request(response):
    datastore.close_datastore()
    app.logger.debug('after_request')
    return response

@app.route('/init')
def load():
    filenames = next(walk(app.config['UPLOAD_PATH']), (None, None, []))[2]  # [] if no file
    for filename in filenames:
        file_path = path.join(app.config['UPLOAD_PATH'], filename)
        app.logger.debug('file_path:' + file_path)
        datastore.store_df(filename, pd.read_csv(file_path))
    return {'filenames': filenames}

@app.route('/uploader', methods = ['POST'])
def upload_file():
    app.logger.debug('request:' + str(request))
    app.logger.debug('request.files:' + str(request.files))
    app.logger.debug('request.headers' + str(request.headers))
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    file_path = path.join(app.config['UPLOAD_PATH'], filename)
    if filename != '':
        file_ext = path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "\n Not a csv", 400
        uploaded_file.save(file_path)
        datastore.store_df(filename, pd.read_csv(file_path))
        remove(file_path)
        #Return the entire dataframe as a json
        #return pandas_func.df_to_json(datastore.get_df(filename))

        #Return head of first 1,000 rows as json
        return head_or_tail(file_name, 'head', app.config['MAX_HEADER_ROWS'])
    return "\n No file attached", 400

#todo 
@app.route("/downloader/<file_name>")
def get_file(file_name):
    df = datastore.get_df(file_name)
    csv_string = df.to_csv()
    return {'data': csv_string}
        
@app.route('/pandas/head/<string:file_name>/<int:n>')
def get_head(file_name, n):
    return head_or_tail(file_name, 'head', n)

@app.route('/pandas/tail/<string:file_name>/<int:n>')
def get_tail(file_name, n):
    return head_or_tail(file_name, 'tail', n)

@app.route('/pandas/rm_dups/<string:file_name>/<string:column_name>')
def remove_duplicates(file_name, column_name):
    try: 
        df = datastore.get_df(file_name)
        json = pandas_func.remove_duplicates(df, column_name)
        datastore.lpush(file_name, 'remove_duplicates:' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/get_dummies/<string:file_name>/<string:column_name>')
def get_dummies(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.getDummies(df, file_name, column_name)
        datastore.lpush(file_name, 'get_dummies' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404

@app.route('/pandas/rm_nulls/<string:file_name>/<string:column_name>')
def remove_nulls(file_name, column_name):
    try: 
        df = datastore.get_df(file_name)
        json = pandas_func.remove_nulls(df, column_name)
        datastore.lpush(file_name, 'remove_nulls:' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace/na_mean/<string:file_name>/<string:column_name>')
def replace_na_mean(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.replace_na_numeric(df, column_name, 'mean')
        datastore.lpush(file_name, 'replace_na_man:' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace/na_median/<string:file_name>/<string:column_name>')
def replace_na_median(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.replace_na_numeric(df, column_name, 'median')
        datastore.lpush(file_name, 'replace_na_median:' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace/na_mode_numeric/<string:file_name>/<string:column_name>')
def replace_na_mode_numeric(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.replace_na_numeric(df, column_name, 'mode')
        datastore.lpush(file_name, 'replace_na_mode_numeric:' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace/na_unknown/<string:file_name>/<string:column_name>')
def replace_na_unknown(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.replace_na_categorical(df, column_name, 'unknown')
        datastore.lpush(file_name, 'remove_na_unknown:' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404         

@app.route('/pandas/replace/na_ffill/<string:file_name>/<string:column_name>')
def replace_na_ffill(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.replace_na_categorical(df, column_name, 'ffill')
        datastore.lpush(file_name, 'replace_na_ffill:' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

@app.route('/pandas/replace/na_bfill/<string:file_name>/<string:column_name>')
def replace_na_bfill(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.replace_na_categorical(df, column_name, 'bfill')
        datastore.lpush(file_name, 'replace_na_bfill:' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

@app.route('/pandas/replace/na_mode_categorical/<string:file_name>/<string:column_name>')
def replace_na_mode_categorical(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.replace_na_categorical(df, column_name, 'mode')
        datastore.lpush(file_name, 'replace_na_mode_categorical:' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

@app.route('/pandas/rename_column/<string:file_name>/<string:old_column>/<string:new_column>')
def rename_column(file_name, old_column, new_column):
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.rename(df, old_column, new_column)
        datastore.lpush(file_name, 'rename_column:' + old_column + ':' + new_column, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404

@app.route('/pandas/normalize/<string:file_name>/<string:column_name>')
def normalize(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.normalize(df, column_name)
        datastore.lpush(file_name, 'normalize:' + column_name, df)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404

@app.errorhandler(413)
def too_large(e):
    return "\nFile is too large", 413

if __name__ == "__main__":
    app.run()

def head_or_tail(file_name, direction, n):
    if n > app.config['MAX_HEADER_ROWS']:
        return '\n Exceeds max configured records' , 404
    try:
        df = datastore.get_df(file_name)
        json = pandas_func.view_dataframe(df, direction, n)
        return '\n' + json, 200
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

# structure of steps would be linkedlist of Steps
# [ [rename_column, old_column_name, new_column_name], [normalize, column_name] .... ]
# currently we have up to 2 parameters max
# The parameters must be in order
# def invokeSteps(listOfSteps, file_name):
#     for step in listOfSteps:
#         if (step.length == 2):
#             paramOne = step.paramOne
#             locals()[step.functionName](file_name, step.paramOne)
#         if (step.length == 3):
#             locals()[step.functionName](file_name, step.paramOne, step.paramTwo)
#         else:
#             locals()[step.functionName](file_name)
