from flask import Flask
from pandas.testing import assert_frame_equal 
import pandas as pd
import unittest
import pandas_func

app = Flask(__name__)

def read_csv(filename):
    return pd.read_csv('../csv/' + filename)

class TestPandas(unittest.TestCase):

    def setUp(self):
        ctx = app.app_context()
        ctx.push()

    def test_view_dataframe_head(self):
        dataframe_123csv = read_csv('123.csv')
        dataframe_actual = pandas_func.view_dataframe(dataframe_123csv, 'head', 1)
        dataframe_expected = dataframe_123csv.head(1) 
        assert_frame_equal(dataframe_actual, dataframe_expected)
    
    def test_view_dataframe_tail(self):
        dataframe_123csv = read_csv('123.csv')
        dataframe_actual = pandas_func.view_dataframe(dataframe_123csv, 'tail', 1)
        dataframe_expected = dataframe_123csv.tail(1) 
        assert_frame_equal(dataframe_actual, dataframe_expected)

    def test_export_to_csv(self):
        assert 1 == 0, "TODO"

    def test_get_dummies(self):
        assert 1 == 0, "TODO"

    def test_remove_duplicates(self):
        dataframe_duplicates = read_csv('test_files/remove_duplicates.csv')
        dataframe_actual = pandas_func.remove_duplicates(dataframe_duplicates, 'c')
        dataframe_expected = dataframe_duplicates.head(1)
        assert_frame_equal(dataframe_actual, dataframe_expected)

    def test_remove_nulls(self):
        dataframe_nulls = read_csv('test_files/drop_null.csv')
        dataframe_actual = pandas_func.remove_nulls(dataframe_nulls, 'a')
        dataframe_expected = dataframe_nulls.tail(1)
        assert_frame_equal(dataframe_actual, dataframe_expected)

    def test_rename(self):
        dataframe = read_csv('cereal.csv')
        dataframe_actual = pandas_func.rename(dataframe, 'mfr', 'abc')
        actual_column_name = list(dataframe_actual.columns)[1]
        expected_column_name = 'abc'
        assert actual_column_name == expected_column_name, "Column name should be changed to abc"

    def test_replace_na_mean(self):
        dataframe = read_csv('test_files/mean.csv')
        dataframe_actual = pandas_func.replace_na_numeric(dataframe, 'a', 'mean')
        actual = dataframe_actual['a'].values[0]
        expected = 2.5
        assert actual == expected, "NA value should be replaced with mean"

    def test_replace_na_median(self):
        dataframe = read_csv('test_files/median.csv')
        dataframe_actual = pandas_func.replace_na_numeric(dataframe, 'a', 'median')
        actual = dataframe_actual['a'].values[0]
        expected = 3.0
        assert actual == expected, "NA value should be replaced with median"

    def test_replace_na_mode(self):
        dataframe = read_csv('test_files/mode.csv')
        dataframe_actual = pandas_func.replace_na_numeric(dataframe, 'a', 'mode')
        actual = dataframe_actual['a'].values[0]
        expected = 1
        assert actual == expected, "NA value should be replaced with mode"
    
    def test_replace_categorical_unknown(self):
        assert 1 == 0, "TODO"

    def test_replace_categorical_ffill(self):
        assert 1 == 0, "TODO"

    def test_replace_categorical_bfill(self):
        assert 1 == 0, "TODO"

    def test_replace_categorical_mode(self):
        assert 1 == 0, "TODO"    

    def test_normalize(self):
        assert 1 == 0, "TODO"

    def test_value_editor(self):
        assert 1 == 0, "TODO"

    def test_quartile_trimmer(self):
        assert 1 == 0, "TODO"
    
    def test_date_transformer(self):
        assert 1 == 0, "TODO"
    
    def test_transformer(self):
        assert 1 == 0, "TODO"

if __name__ == '__main__':
    unittest.main()

# def view_dataframe(df, direction, n):
#     if direction == 'head':
#         json_string = df.head(n).to_json(orient='records')
#     else:
#         json_string = df.tail(n).to_json(orient='records')
#     return json.dumps(json.loads(json_string), indent=4)

# def export(jsonString):
#     df = pd.read_json(jsonString)
#     df = df.drop(df.columns[[0]], axis=1)
#     df.to_csv("../csv/exported.csv")

# # Transform categorical variable column into mulitple binary predictors
# def getDummies(df, col_name):
#     df = pd.read_csv(os.path.join(path, file_name))
#     if df[col_name].nunique() < 45:
#         df1 = pd.get_dummies(df[col_name])
#         df2 = df.drop(col_name, axis=1)
#         df3 = df2.join(df1)
#         return json.dumps(json.loads(df3.to_json(orient='records')))
#     else:
#         return "Error - too many variables"

# # """Remove duplicates given a column index, method is optional for keeping first or last"""
# def remove_duplicates(df, col_name, method="first"):
#     if df[col_name].duplicated().values.any():
#         df = df.drop_duplicates(subset=col_name, keep=method)
#         return json.dumps(json.loads(df.to_json(orient='records')))
#     else:
#         return "No Duplicates"

# # """Remove nulls given a column index"""
# def remove_nulls(df, col_name):
#     if df[col_name].isna().values.any():
#         df = df.dropna(subset=col_name)
#         return json.dumps(json.loads(df.to_json(orient='records')))
#     else:
#         return "No Nulls"

# # """Rename column name into new column name"""
# def rename(df, old_name, new_name):
#     df.rename(columns = {old_name:new_name}, inplace = True)
#     return json.dumps(json.loads(df.to_json(orient='records')))

# # """This function should only be used for numeric columns. Replace Na stat with mean median or mode can later add regressions and fancy stuff as well to here. Probably call another function"""
# def replace_na_numeric(df, col_name, stat):
#     if stat == 'mean':
#         df[col_name].fillna(value=df[col_name].mean(), inplace=True)
#     if stat == 'mode':
#         df[col_name].fillna(value=df[col_name].mode(), inplace=True)
#     elif stat == 'median':
#         df[col_name].fillna(value=df[col_name].median(), inplace=True)
#     return json.dumps(json.loads(df.to_json(orient='records')))

# # """This function should be used to treat nulls in categorical columns""""
# def replace_na_categorical(df, col_name, stat):
#     if stat == "unknown":
#         df[col_name].fillna("unknown", inplace = True)
#     if stat == 'ffill':
#         df[col_name].fillna(method = "ffill", limit = 1, inplace = True)
#     if stat == 'bfill':
#         df[col_name].fillna(method = "bfill", limit = 1, inplace = True)
#     if stat == 'mode':
#         df[col_name] = df[col_name].fillna( df[col_name].mode()[0])
#     return json.dumps(json.loads(df.to_json(orient='records')))

# # """"Normalize Column"""
# def normalize_column(df, col_name):
#     df_max_scaled = df.copy()
#     df_max_scaled[col_name] = df_max_scaled[col_name] /df_max_scaled[col_name].abs().max()
#     return json.dumps(json.loads(df_max_scaled.to_json(orient='records')))

