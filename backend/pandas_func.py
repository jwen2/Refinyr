from sklearn import preprocessing
import pandas as pd
import os
import matplotlib as mb
from flask import current_app as app
from scipy import stats

def view_dataframe(df, direction, n):
    app.logger.info('View dataframe %s %d', direction, n)
    if direction == 'head':
        return df.head(n)
    else:
        return df.tail(n)

def export(jsonString):
    app.logger.info('Export json string')
    df = pd.read_json(jsonString)
    df = df.drop(df.columns[[0]], axis=1)
    df.to_csv("../csv/exported.csv")

# Transform categorical variable column into mulitple binary predictors
def getDummies(df, col_name):
    app.logger.info('Get dummies for column %s', col_name)
    df = pd.read_csv(os.path.join(path, file_name))
    if df[col_name].nunique() < 45:
        df1 = pd.get_dummies(df[col_name])
        df2 = df.drop(col_name, axis=1)
        df3 = df2.join(df1)
        return df3
    else:
        return "Error - too many variables"

# """Remove duplicates given a column index, method is optional for keeping first or last"""
def remove_duplicates(df, col_name, method="first"):
    app.logger.info('Remove duplicates for column %s', col_name)
    df = df.copy(deep=True)
    if df[col_name].duplicated().values.any():
        df = df.drop_duplicates(subset=col_name, keep=method)
        return df
    else:
        return "No Duplicates"

# """Remove nulls given a column index"""
def remove_nulls(df, col_name):
    if df[col_name].isna().values.any():
        df = df.dropna(subset=[col_name])
        return df
    else:
        return "No Nulls"

# """Rename column name into new column name"""
def rename(df, old_name, new_name):
    app.logger.info('Rename column %s to %s', old_name, new_name)
    df = df.copy(deep=True)
    df.rename(columns = {old_name:new_name}, inplace = True)
    return df

# """This function should only be used for numeric columns. Replace Na stat with mean median or mode can later add regressions and fancy stuff as well to here. Probably call another function"""
def replace_na_numeric(df, col_name, stat):
    app.logger.info('Replace NA numeric %s %s', col_name, stat)
    df = df.copy(deep=True)
    if stat == 'mean':
        df[col_name].fillna(value=df[col_name].mean(), inplace=True)
    if stat == 'mode':
        df[col_name].fillna(value=df[col_name].mode(), inplace=True)
    elif stat == 'median':
        df[col_name].fillna(value=df[col_name].median(), inplace=True)
    return df

# """This function should be used to treat nulls in categorical columns""""
def replace_na_categorical(df, col_name, stat):
    app.logger.info('Replace NA categorical %s %s', col_name, stat)
    df = df.copy(deep=True)
    if stat == "unknown":
        df[col_name].fillna("unknown", inplace = True)
    if stat == 'ffill':
        df[col_name].fillna(method = "ffill", limit = 1, inplace = True)
    if stat == 'bfill':
        df[col_name].fillna(method = "bfill", limit = 1, inplace = True)
    if stat == 'mode':
        df[col_name] = df[col_name].fillna( df[col_name].mode()[0])
    return df

# """"Normalize Column"""
def normalize_column(df, col_name):
    app.logger.info('Normalize column %s', col_name)
    df_max_scaled = df.copy()
    df_max_scaled[col_name] = df_max_scaled[col_name] /df_max_scaled[col_name].abs().max()
    return df_max_scaled

### use this function to batch edit from the UI.

def value_editor(df, col_name, old_value, new_value):
    app.logger.info('View editor %s %s %s', col_name, old_value, new_value)
    df = df.copy(deep=True)
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
    app.logger.info('Quartile trimmer %s %d', col_name, n)
    df = df.copy(deep=True)
    transformed = "clipped_" + col_name
    upper = df[col_name].quantile(1-n)
    lower = df[col_name].quantile(n)
    df[transformed] = df[col_name].clip(lower, upper, axis = 0)
    return df


#### date transformer, extracts specific information from a specific date variable.
### can extract day, month, year, quarter, dayofweek, weekday in text.
### t = type of date transformation

def dateTransformer(df, col_name, t):
    app.logger.info('Date transformer %s', col_name)
    df = df.copy(deep=True)
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
    app.logger.info('Transformer %s %s', col_name, x)
    df = df.copy(deep=True)
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

#have to import a new popular library scipy.
#takes in a dataframe and a column
#outputs updates the dataframe to remove the outlier rows from the dataframe
#operates similar to remove duplicates, and remove nulls
def remove_outliers(df, col_name):
    z_scores = stats.zscore(df[col_name])
    abs_z_scores = np.abs(z_scores)
    filtered = (abs_z_scores < 3)
    updated_df = df[filtered]
    return updated_df



def histogram (df, col_name):
    app.logger.info('Histogram %s', col_name)
    return df[col_name].hist()
