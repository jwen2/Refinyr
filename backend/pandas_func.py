from sklearn import preprocessing
import pandas as pd
import json
import os
import matplotlib as mb

def view_dataframe(df, direction, n):
    if direction == 'head':
        json_string = df.head(n).to_json(orient='records')
    else:
        json_string = df.tail(n).to_json(orient='records')
    return json.dumps(json.loads(json_string), indent=4)

def export(jsonString):
    df = pd.read_json(jsonString)
    df = df.drop(df.columns[[0]], axis=1)
    df.to_csv("../csv/exported.csv")

# Transform categorical variable column into mulitple binary predictors
def getDummies(df, col_name):
    df = pd.read_csv(os.path.join(path, file_name))
    if df[col_name].nunique() < 45:
        df1 = pd.get_dummies(df[col_name])
        df2 = df.drop(col_name, axis=1)
        df3 = df2.join(df1)
        return json.dumps(json.loads(df3.to_json(orient='records')))
    else:
        return "Error - too many variables"

# """Remove duplicates given a column index, method is optional for keeping first or last"""
def remove_duplicates(df, col_name, method="first"):
    if df[col_name].duplicated().values.any():
        df = df.drop_duplicates(subset=col_name, keep=method)
        return json.dumps(json.loads(df.to_json(orient='records')))
    else:
        return "No Duplicates"

# """Remove nulls given a column index"""
def remove_nulls(df, col_name):
    if df[col_name].isna().values.any():
        df = df.dropna(subset=col_name)
        return json.dumps(json.loads(df.to_json(orient='records')))
    else:
        return "No Nulls"

# """Rename column name into new column name"""
def rename(df, old_name, new_name):
    df.rename(columns = {old_name:new_name}, inplace = True)
    return json.dumps(json.loads(df.to_json(orient='records')))

# """This function should only be used for numeric columns. Replace Na stat with mean median or mode can later add regressions and fancy stuff as well to here. Probably call another function"""
def replace_na_numeric(df, col_name, stat):
    if stat == 'mean':
        df[col_name].fillna(value=df[col_name].mean(), inplace=True)
    if stat == 'mode':
        df[col_name].fillna(value=df[col_name].mode(), inplace=True)
    elif stat == 'median':
        df[col_name].fillna(value=df[col_name].median(), inplace=True)
    return json.dumps(json.loads(df.to_json(orient='records')))

# """This function should be used to treat nulls in categorical columns""""
def replace_na_categorical(df, col_name, stat):
    if stat == "unknown":
        df[col_name].fillna("unknown", inplace = True)
    if stat == 'ffill':
        df[col_name].fillna(method = "ffill", limit = 1, inplace = True)
    if stat == 'bfill':
        df[col_name].fillna(method = "bfill", limit = 1, inplace = True)
    if stat == 'mode':
        df[col_name] = df[col_name].fillna( df[col_name].mode()[0])
    return json.dumps(json.loads(df.to_json(orient='records')))

# """"Normalize Column"""
def normalize_column(df, col_name):
    df_max_scaled = df.copy()
    df_max_scaled[col_name] = df_max_scaled[col_name] /df_max_scaled[col_name].abs().max()
    return json.dumps(json.loads(df_max_scaled.to_json(orient='records')))



### use this function to batch edit from the UI.

def value_editor(df, col_name, old_value, new_value):
    if old_value in df[col_name].unique():
        NewColumn = df[col_name].replace({old_value : new_value})
        Newdf = df
        Newdf[col_name] = NewColumn
        return Newdf
    else:
        return ("Error could not find value")

### use this function to trim the ends of a column
### useful for treating outliers
### recommended n's (0.01 for 99% confidence)
###                 (0.05 for 95% confidence)
###                 (0.10 for 90% confidence)


def quartile_trimmer(df, col_name, n):
    transformed = "clipped_" + col_name
    upper = df[col_name].quantile(1-n)
    lower = df[col_name].quantile(n)
    df[transformed] = df[col_name].clip(lower, upper, axis = 0)
    return df


#### date transformer, extracts specific information from a specific date variable.
### can extract day, month, year, quarter, dayofweek, weekday in text.
### t = type of date transformation

def dateTransformer(df, col_name, t):
    df[col_name] = pd.to_datetime(df[col_name])
    if t == 'day':
        df[col_name+"_day"] = df[col_name].dt.day
        return df
    elif t == 'month':
        df[col_name+"_month"] = df[col_name].dt.month
        return df
    elif t == 'year':
        df[col_name+"_year"] = df[col_name].dt.year
        return df
    elif t == 'quarter':
        df[col_name+"_quarter"] = df[col_name].dt.quarter
        return df
    elif t == 'dayofweek':
        df[col_name+"_dayofweek"] = df[col_name].dt.dayofweek
        return df
    elif t == 'weekday':
        df[col_name+"_weekday"] = df[col_name].dt.day_name()
        return df
    else:
        return df

def transformer(df, col_name, x):
    if df[col_name].dtypes == "int64":
        if x == "squared":
            df[col_name+"_squared"] = df[col_name] * df[col_name]
            return (df)
        if x == "log":
            df[col_name+"_ln"] = np.log(df[col_name])
            return (df)
        if x == "root2":
            df[col_name+"_root2"] = np.sqrt(df[col_name])
            return (df)
    else:
        return ("Can not apply transformation to none numeric column")


def histogram (df, col_name):
    return df[col_name].hist()

def df_to_json(df):
    return json.dumps(json.loads(df.to_json(orient='records')))
