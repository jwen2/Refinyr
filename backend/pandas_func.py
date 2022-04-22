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

#def remove_duplicates(path, file_name, col_name):
#    df = pd.read_csv(os.path.join(path, file_name))
#    df = df.drop_duplicates(subset=[col_name])
#    return json.dumps(json.loads(df.to_json(orient='records')))


#def remove_na(path, file_name, col_name):
#    df = pd.read_csv(os.path.join(path, file_name))
#    return json.dumps(json.loads(df[col_name].fillna(0).to_json(orient='records')))

#def replace_na_stat(path, file_name, col_name, stat):
#    df = pd.read_csv(os.path.join(path, file_name))
#    if stat == 'mean':
#        df[col_name].fillna(value=df[col_name].mean(), inplace=True)
#    elif stat == 'median':
#        df[col_name].fillna(value=df[col_name].median(), inplace=True)
#    return json.dumps(json.loads(df.to_json(orient='records')))

#not working right :D
#def normalize_column(path, file_name, col_name):
#    df = pd.read_csv(os.path.join(path, file_name))
#    x = df.values #returns a numpy array
#    min_max_scaler = preprocessing.MinMaxScaler()
#    x_scaled = min_max_scaler.fit_transform(x)
#    df = pd.DataFrame(x_scaled)
#    return json.dumps(json.loads(df.to_json(orient='records')))

#ruh-roh



"""Transform categorical variable column into mulitple binary predictors"""


def getdummies(df,col_name):
    if df[col_name].nunique() < 45:
        df1 = pd.get_dummies(df[col_name])
        df2 = df.drop(col_name, axis=1)
        df3 = df2.join(df1)
        return(df3)
    else:
        return "Error - too many variables"

"""Remove duplicates given a column index, method is optional for keeping first or last"""

def remove_duplicates(df, col_name, method="first"):
    if df[col_name].duplicated().values.any():
        df = df.drop_duplicates(subset=col_name, keep=method)
        return (df)
    else:
        return "No Duplicates"

"""Remove nulls given a column index"""

def remove_nulls(df,col_name):
    if df[col_name].isna().values.any():
        df = df.dropna(subset=col_name)
        return (df)
    else:
        return "No Nulls"


"""Rename column name into new column name"""
def rename (df, col_name, new_name):
    df.rename(columns = {col_name:new_name}, inplace = True)
    return(df)

"""This function should only be used for numeric columns. Replace Na stat with mean median or mode can later add regressions and fancy stuff as well to here. Probably call another function"""

def replace_na_Numeric(df, col_name, stat):
    if stat == 'mean':
        df[col_name].fillna(value=df[col_name].mean(), inplace=True)
    if stat == 'mode':
        df[col_name].fillna(value=df[col_name].mode(), inplace=True)
    elif stat == 'median':
        df[col_name].fillna(value=df[col_name].median(), inplace=True)
    return (df)

"""This function should be used to treat nulls in categorical columns""""

def replace_na_Categorical(df, col_name, stat):
    if stat == "unknown":
        df[col_name].fillna("unknown", inplace = True)
    if stat == 'ffill':
        df[col_name].fillna(method = "ffill", limit = 1, inplace = True)
    if stat == 'bfill':
        df[col_name].fillna(method = "bfill", limit = 1, inplace = True)
    if stat == 'mode':
        df[col_name] = df[col_name].fillna( df[col_name].mode()[0])
    return (df)

""""Normalize Column"""

def normalize_column(df, col_name):
    df_max_scaled = df.copy()
    df_max_scaled[col_name] = df_max_scaled[col_name] /df_max_scaled[col_name].abs().max()
    return (df_max_scaled)
