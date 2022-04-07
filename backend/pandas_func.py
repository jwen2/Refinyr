from sklearn import preprocessing
import pandas as pd
import json
import os

def view_dataframe(path, file_name, direction, n):
    df = pd.read_csv(os.path.join(path, file_name))
    if direction == 'head':
        json_string = df.head(n).to_json(orient='records')
    else:
        json_string = df.tail(n).to_json(orient='records')
    return json.dumps(json.loads(json_string), indent=4)

def remove_duplicates(path, file_name, column_name):
    df = pd.read_csv(os.path.join(path, file_name))
    df = df.drop_duplicates(subset=[column_name])
    return json.dumps(json.loads(df.to_json(orient='records')))

def remove_na(path, file_name, column_name):
    df = pd.read_csv(os.path.join(path, file_name))
    return json.dumps(json.loads(df[column_name].fillna(0).to_json(orient='records')))

def replace_na_stat(path, file_name, column_name, stat):
    df = pd.read_csv(os.path.join(path, file_name))
    if stat == 'mean':
        df[column_name].fillna(value=df[column_name].mean(), inplace=True)
    elif stat == 'median':
        df[column_name].fillna(value=df[column_name].median(), inplace=True)
    return json.dumps(json.loads(df.to_json(orient='records')))    

#<<<<< Methods implemented up to here
#not working right :D
def normalize_column(path, file_name, column_name):
    df = pd.read_csv(os.path.join(path, file_name))
    x = df.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled)
    return json.dumps(json.loads(df.to_json(orient='records')))    

#ruh-roh
def one_hot_encoder(path, file_name, column_name):
    pass