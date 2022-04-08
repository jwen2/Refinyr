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

#def remove_duplicates(path, file_name, column_name):
#    df = pd.read_csv(os.path.join(path, file_name))
#    df = df.drop_duplicates(subset=[column_name])
#    return json.dumps(json.loads(df.to_json(orient='records')))


#def remove_na(path, file_name, column_name):
#    df = pd.read_csv(os.path.join(path, file_name))
#    return json.dumps(json.loads(df[column_name].fillna(0).to_json(orient='records')))

#def replace_na_stat(path, file_name, column_name, stat):
#    df = pd.read_csv(os.path.join(path, file_name))
#    if stat == 'mean':
#        df[column_name].fillna(value=df[column_name].mean(), inplace=True)
#    elif stat == 'median':
#        df[column_name].fillna(value=df[column_name].median(), inplace=True)
#    return json.dumps(json.loads(df.to_json(orient='records')))

#not working right :D
#def normalize_column(path, file_name, column_name):
#    df = pd.read_csv(os.path.join(path, file_name))
#    x = df.values #returns a numpy array
#    min_max_scaler = preprocessing.MinMaxScaler()
#    x_scaled = min_max_scaler.fit_transform(x)
#    df = pd.DataFrame(x_scaled)
#    return json.dumps(json.loads(df.to_json(orient='records')))

#ruh-roh
def one_hot_encoder(path, file_name, column_name):
    pass

"""Transform categorical variable column into mulitple binary predictors"""

def getdummies(df,col_index):
    if df.iloc[:, col_index].nunique() < 45:
        df1 = pd.get_dummies(df.iloc[:, col_index])
        df2 = df.drop(df.columns[[col_index]], axis=1)
        df3 = df2.join(df1)
        return(df3)
    else:
        return "Error - too many variables"

"""Remove duplicates given a column index"""

def remove_duplicates(df,col_index):
    if df.iloc[:, col_index].duplicated().values.any():
        col_name = df.columns[col_index]
        df = df.drop_duplicates(subset=col_name)
        return (df)
    else:
        return "No Duplicates"

"""Remove nulls given a column index"""

def remove_nulls(df,col_index):
    if df.iloc[:, col_index].isna().values.any():
        col_name = df.columns[col_index]
        df = df.dropna(subset=col_name)
        return (df)
    else:
        return "No Nulls"


"""Rename column name into new column name"""
def rename (df, old_name, new_name):
    df.rename(columns = {old_name:new_name}, inplace = True)
    return(df)

"""Replace Na stat with mean median or mode can later add regressions and fancy stuff as well to here. Probably call another function""""

def replace_na_stat(df, column_name, stat):
    if stat == 'mean':
        df[column_name].fillna(value=df[column_name].mean(), inplace=True)
    if stat == 'mode':
        df[column_name].fillna(value=df[column_name].mode(), inplace=True)
    elif stat == 'median':
        df[column_name].fillna(value=df[column_name].median(), inplace=True)
    return (df)


""""Normalize Column"""

def normalize_column(df, column_name):
    df_max_scaled = df.copy()
    df_max_scaled[column_name] = df_max_scaled[column_name] /df_max_scaled[column_name].abs().max()
    return (df_max_scaled)
