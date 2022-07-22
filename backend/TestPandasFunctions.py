from flask import Flask
from pandas.testing import assert_frame_equal, assert_series_equal
import pandas as pd
import unittest
import pandas_func
import json

app = Flask(__name__)

def read_csv(filename):
    return pd.read_csv('../csv/' + filename)

def df_to_json(df):
    li = []
    df['DisbursalDate'] = df['DisbursalDate'].dt.strftime('%Y-%m-%d')
    df_to_json = df.to_json(orient='records', date_format='iso')
    print(df_to_json)
    json_loads_json = json.loads(df_to_json)
    print(json.dumps(json_loads_json, indent=4, sort_keys=True))
    li.append(json_loads_json)
    li.append(pandas_func.addDataTypeToHeader(df))
    return json.dumps(li)

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
        dataframe = read_csv('test_files/replace_categorical_unknown.csv')
        dataframe_actual = pandas_func.replace_na_categorical(dataframe, 'a', 'unknown')
        actual = dataframe_actual['a'].values[1]
        assert actual == 'unknown', "NaN value replaced with unknown"

    def test_replace_categorical_ffill(self):
        dataframe = read_csv('test_files/replace_categorical_unknown.csv')
        dataframe_actual = pandas_func.replace_na_categorical(dataframe, 'a', 'ffill')
        actual = dataframe_actual['a'].values[1]
        assert actual == 'aa', "NaN value replaced with previous value"

    def test_replace_categorical_bfill(self):
        dataframe = read_csv('test_files/replace_categorical_unknown.csv')
        dataframe_actual = pandas_func.replace_na_categorical(dataframe, 'a', 'bfill')
        actual = dataframe_actual['a'].values[1]
        assert actual == 'ff', "NaN value replaced with forward value"

    def test_normalize(self):
        dataframe = read_csv('test_files/normalize.csv')
        series_actual = pandas_func.normalize_column(dataframe, 'a')['a']
        series_expected = dataframe['a'] / 5
        assert_series_equal(series_actual, series_expected)

    def test_value_editor(self):
        dataframe = read_csv('test_files/value_editor.csv')
        series_actual = pandas_func.value_editor(dataframe, 'a', 'd', 'a')['a']
        assert_series_equal(series_actual, pd.Series(['a','a','a'], name='a'))

    def test_quartile_trimmer(self):
        assert 1 == 0, "TODO"
    
    def test_date_transformer(self):
        assert 1 == 0, "TODO"
    
    def test_transformer(self):
        assert 1 == 0, "TODO"

    def test_date(self):
        dataframe = read_csv('test_files/datetest.csv')
        actual_dataframe = pandas_func.change_data_type(dataframe, 'DisbursalDate', 'to_date')
        df_to_json(actual_dataframe)
        
if __name__ == '__main__':
    unittest.main()