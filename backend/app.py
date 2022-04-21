from flask import Flask, request, abort, send_from_directory
import os
import pandas_func

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['UPLOAD_PATH'] = '../csv'
app.config['MAX_HEADER_ROWS'] = 100


@app.route('/hello')
def load():
    return '\n hello'

@app.route('/uploader', methods = ['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "\n Not a csv", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return "\n Saved", 200
    return "\n No file attached", 400

@app.route("/downloader/<file_name>")
def get_image(file_name):
    try:
        return send_from_directory(directory=app.config["UPLOAD_PATH"], path=file_name)
    except FileNotFoundError:
        abort(404)        
        
@app.route('/pandas/head/<string:file_name>/<int:n>')
def get_head(file_name, n):
    return head_or_tail(file_name, 'head', n)

@app.route('/pandas/tail/<string:file_name>/<int:n>')
def get_tail(file_name, n):
    return head_or_tail(file_name, 'tail', n)

@app.route('/pandas/rm_dups/<string:file_name>/<string:column_name>')
def remove_duplicates(file_name, column_name):
    try: 
        json = pandas_func.remove_duplicates(app.config['UPLOAD_PATH'], file_name, column_name)
        pandas_func.export(json)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/get_dummies/<string:file_name>/<string:column_name>')
def get_dummies(file_name, column_name):
    try:
        json = pandas_func.getDummies(app.config['UPLOAD_PATH'], file_name, column_name)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404

@app.route('/pandas/rm_nulls/<string:file_name>/<string:column_name>')
def remove_nulls(file_name, column_name):
    try: 
        json = pandas_func.remove_nulls(app.config['UPLOAD_PATH'], file_name, column_name)
        pandas_func.export(json)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace/na_mean/<string:file_name>/<string:column_name>')
def replace_na_mean(file_name, column_name):
    try:
        json = pandas_func.replace_na_numeric(app.config['UPLOAD_PATH'], file_name, column_name, 'mean')
        pandas_func.export(json)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace/na_median/<string:file_name>/<string:column_name>')
def replace_na_median(file_name, column_name):
    try:
        json = pandas_func.replace_na_numeric(app.config['UPLOAD_PATH'], file_name, column_name, 'median')
        pandas_func.export(json)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace/na_mode_numeric/<string:file_name>/<string:column_name>')
def replace_na_mode_numeric(file_name, column_name):
    try:
        json = pandas_func.replace_na_numeric(app.config['UPLOAD_PATH'], file_name, column_name, 'mode')
        pandas_func.export(json)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404 

@app.route('/pandas/replace/na_unknown/<string:file_name>/<string:column_name>')
def replace_na_unknown(file_name, column_name):
    try:
        json = pandas_func.replace_na_categorical(app.config['UPLOAD_PATH'], file_name, column_name, 'unknown')
        pandas_func.export(json)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404         

@app.route('/pandas/replace/na_ffill/<string:file_name>/<string:column_name>')
def replace_na_ffill(file_name, column_name):
    try:
        json = pandas_func.replace_na_categorical(app.config['UPLOAD_PATH'], file_name, column_name, 'ffill')
        pandas_func.export(json)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

@app.route('/pandas/replace/na_bfill/<string:file_name>/<string:column_name>')
def replace_na_bfill(file_name, column_name):
    try:
        json = pandas_func.replace_na_categorical(app.config['UPLOAD_PATH'], file_name, column_name, 'bfill')
        pandas_func.export(json)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

@app.route('/pandas/replace/na_mode_categorical/<string:file_name>/<string:column_name>')
def replace_na_mode_categorical(file_name, column_name):
    try:
        json = pandas_func.replace_na_categorical(app.config['UPLOAD_PATH'], file_name, column_name, 'mode')
        pandas_func.export(json)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

@app.route('/pandas/rename_column/<string:file_name>/<string:old_column>/to/<string:new_column>')
def rename_column(file_name, old_column_name, new_column_name):
    try:
        json = pandas_func.rename(app.config['UPLOAD_PATH'], file_name, old_column_name, new_column_name)
        return json, 200
    except KeyError:
        return "\n Invalid column name.", 404
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404

@app.route('pandas/normalize/<string:file_name>/<string:column_name')
def normalize(file_name, column_name):
    try:
        json = pandas_func.normalize(app.config['UPLOAD_PATH'], file_name, column_name)
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
        json = pandas_func.view_dataframe(app.config['UPLOAD_PATH'], file_name, direction, n)
        return '\n' + json, 200
    except FileNotFoundError:
        return '\n File not found ' + file_name, 404     

# structure of steps would be linkedlist of lists 
# [[function, <Optional> param1, <Optional> param2....], ....]
# [ [rename_column, old_column_name, new_column_name], [normalize, column_name] .... ]
# currently we have up to 2 parameters max
# The parameters must be in order
def invokeSteps(listOfSteps, file_name):
    for step in listOfSteps:
        functionName = step[0]
        if (step.len() == 2):
            paramOne = step[1]
            locals()[functionName](file_name, paramOne)
        if (step.len() == 3):
            paramOne = step[1]
            paramTwo = step[2]
            locals()[functionName](file_name, paramOne, paramTwo)
        else:
            locals()[functionName](file_name)
