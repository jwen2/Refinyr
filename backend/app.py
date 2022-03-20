from flask import Flask, request, abort, send_from_directory, session
import os
import pandas_func
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['UPLOAD_PATH'] = '../csv/'
app.config['MAX_HEADER_ROWS'] = 100
app.secret_key = 'TODO_SECRET_KEY'

USER_UUID_STR = 'user_uuid';

@app.route('/uploader', methods = ['POST'])
def upload_file():
    if USER_UUID_STR not in session:
        session[USER_UUID_STR] = str(uuid.uuid4())

    uploaded_file = request.files['file']
    file_name = uploaded_file.filename
    if file_name != '':
        file_ext = os.path.splitext(file_name)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Not a csv", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], prefix_file_with_uuid(session, file_name)))
        return "Saved", 200
    return "No file attached", 400

@app.route("/downloader/<file_name>")
def download_file(file_name):
    if USER_UUID_STR not in sessions:
        return 'UUID not set', 400
    try:
        return send_from_directory(directory=app.config['UPLOAD_PATH'], path=prefix_file_with_uuid(session, file_name))
    except FileNotFoundError:
        abort(404)        
        
@app.route('/pandas/head/<string:file_name>/<int:n>')
def get_head(file_name, n):
    return head_or_tail(file_name, 'head', n)

@app.route('/pandas/tail/<string:file_name>/<int:n>')
def get_tail(file_name, n):
    return head_or_tail(file_name, 'tail', n)

def head_or_tail(file_name, direction, n):
    if n > app.config['MAX_HEADER_ROWS']:
        return 'Exceeds max configured records' , 404
    try:
        json = pandas_func.view_dataframe(app.config['UPLOAD_PATH'], file_name, direction, n)
        return json, 200
    except FileNotFoundError:
        return 'File not found ' + file_name, 404     

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

def prefix_file_with_uuid(session, file_name):
    return session[USER_UUID_STR] + '_' + file_name

if __name__ == "__main__":
    app.run()         

