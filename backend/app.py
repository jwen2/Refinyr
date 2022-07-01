from flask import Flask, request, abort, send_from_directory, jsonify, g
from io import StringIO
from werkzeug.wrappers import Response
from flask_cors import CORS
from os import walk, path, remove
import pandas_func
import datastore
import pandas as pd
import json
from inspect import getmembers, isfunction
import sys

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
#Path where test csv files are stored
app.config['UPLOAD_PATH'] = '../csv'
app.config['MAX_HEADER_ROWS'] = 1000

#In memory db setup
basedir = path.abspath(path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.before_first_request
def init_db():
    app.logger.debug('before_first_request')
    # Drop all existing tables. Useful if you add/delete columns thru code and want to reflect changes in database.
    # Otherwise comment out drop_all()
    db.drop_all()
    db.create_all()

@app.before_request
def before_request():
    g.current_function = {}
    app.logger.debug('before_request')
    datastore.get_datastore()

@app.after_request
def after_request(response):
    insert_or_update(g.current_function)
    datastore.close_datastore()
    app.logger.debug('after_request')
    return response

#todo should just be update...create a init.sql file and populate table on start up
def insert_or_update(current_function):
    if current_function.get('name') is not None:
        app.logger.debug('insert or update func ' + current_function['name'])
        fn = FunctionStat.query.filter_by(function_name=current_function['name']).first()
        if fn is None:
            app.logger.debug('new function ' + current_function['name'] + ' count 1')
            db.session.add(FunctionStat(function_name=current_function['name'], count=1))
        else:
            fn.count = fn.count + 1
            app.logger.debug('existing function ' + fn.function_name + ' count ' + str(fn.count))
            db.session.add(fn)
        db.session.commit()

@app.route('/getAllFunctions')
def getAllFunctions():
    excluded = ['upload_file', 'load', 'get_file', 'abort', 'head_or_tail', 'too_large', 'walk', 'getmembers', 'isfunction', 'send_from_directory', 'getAllFunctions']
    funcArr = []
    for x in getmembers(sys.modules[__name__], isfunction):
        if (x[0] not in excluded):
            funcArr.append(x[0])
    print(funcArr)
    return jsonify({'funcArr': funcArr}), 200

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
    app.logger.info('Upload file')
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    if filename != '':
        file_ext = path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "\n Not a csv", 400
        file_data = str(uploaded_file.read(), 'UTF-8')
        #print(file_data)
        datastore.store_df(filename, pd.read_csv(StringIO(file_data), sep=','))

        #Return head of first 1,000 rows as json
        return head_or_tail(filename, 'head', app.config['MAX_HEADER_ROWS'])
    return "\n No file attached", 400

#todo 
@app.route("/downloader/<file_name>")
def get_file(file_name):
    df = datastore.get_df(file_name)
    csv_string = df.to_csv()
    return {'data': csv_string}
        
@app.route('/pandas/get_head/<string:file_name>/<int:n>')
def get_head(file_name, n):
    return head_or_tail(file_name, 'head', n)

@app.route('/pandas/get_tail/<string:file_name>/<int:n>')
def get_tail(file_name, n):
    return head_or_tail(file_name, 'tail', n)

@app.route('/pandas/rm_dups/<string:file_name>/<string:column_name>')
def rm_dups(file_name, column_name):
    try: 
        df = datastore.get_df(file_name)
        df = pandas_func.remove_duplicates(df, column_name)
        datastore.lpush(file_name, 'remove_duplicates:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/get_dummies/<string:file_name>/<string:column_name>')
def get_dummies(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.getDummies(df, file_name, column_name)
        datastore.lpush(file_name, 'get_dummies:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404

@app.route('/pandas/rm_nulls/<string:file_name>/<string:column_name>')
def rm_nulls(file_name, column_name):
    try: 
        df = datastore.get_df(file_name)
        df = pandas_func.remove_nulls(df, column_name)
        datastore.lpush(file_name, 'remove_nulls:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace_na_mean/<string:file_name>/<string:column_name>')
def replace_na_mean(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.replace_na_numeric(df, column_name, 'mean')
        datastore.lpush(file_name, 'replace_na_man:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace_na_median/<string:file_name>/<string:column_name>')
def replace_na_median(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.replace_na_numeric(df, column_name, 'median')
        datastore.lpush(file_name, 'replace_na_median:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace_na_mode_numeric/<string:file_name>/<string:column_name>')
def replace_na_mode_numeric(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.replace_na_numeric(df, column_name, 'mode')
        datastore.lpush(file_name, 'replace_na_mode_numeric:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace_na_unknown/<string:file_name>/<string:column_name>')
def replace_na_unknown(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.replace_na_categorical(df, column_name, 'unknown')
        datastore.lpush(file_name, 'remove_na_unknown:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404         

@app.route('/pandas/replace_na_ffill/<string:file_name>/<string:column_name>')
def replace_na_ffill(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.replace_na_categorical(df, column_name, 'ffill')
        datastore.lpush(file_name, 'replace_na_ffill:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

@app.route('/pandas/replace_na_bfill/<string:file_name>/<string:column_name>')
def replace_na_bfill(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.replace_na_categorical(df, column_name, 'bfill')
        datastore.lpush(file_name, 'replace_na_bfill:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

@app.route('/pandas/replace_na_mode_categorical/<string:file_name>/<string:column_name>')
def replace_na_mode_categorical(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.replace_na_categorical(df, column_name, 'mode')
        datastore.lpush(file_name, 'replace_na_mode_categorical:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

@app.route('/pandas/rename_column/<string:file_name>/<string:old_column>/<string:new_column>')
def rename_column(file_name, old_column, new_column):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.rename(df, old_column, new_column)
        datastore.lpush(file_name, 'rename_column:' + old_column + ':' + new_column, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404

@app.route('/pandas/normalize/<string:file_name>/<string:column_name>')
def normalize(file_name, column_name):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.normalize(df, column_name)
        datastore.lpush(file_name, 'normalize:' + column_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404

@app.route('/pandas/do_math/<string:file_name>/<string:column_name>/<string:function_name>')
def do_math(file_name, column_name, function_name):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.transformer(df, column_name, function_name)
        datastore.lpush(file_name, 'do_math:' + column_name + ':' + function_name, df)
        return df_to_json(df), 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404

@app.route('/pandas/change_data_type/<string:file_name>/<string:column_name>/<string:t>')
def change_data_type(file_name, column_name, t):
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.change_data_type(df, column_name, t)
        datastore.lpush(file_name, 'change_data_type:' + column_name + ':' + t, df)
        return df_to_json(df), 200
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
    app.logger.info('head_or_tail %s %s %d', file_name, direction, n)
    if n > app.config['MAX_HEADER_ROWS']:
        return '\n Exceeds max configured records' , 404
    try:
        df = datastore.get_df(file_name)
        df = pandas_func.view_dataframe(df, direction, n)
        return '\n' + df_to_json(df), 200
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     
    except AttributeError:
        return '\n File not found ' + file_name, 404

def df_to_json(df):
    return json.dumps(json.loads(df.to_json(orient='records')))

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


class FunctionStat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    function_name = db.Column(db.String(100), nullable=False)
    count =  db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<FunctionStat {self.function_name}>'