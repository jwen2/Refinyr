import json
import unittest
import pandas_func

class TestPandasFunctions(unittest.TestCase):

    def test_head(self):
        actual_json = pandas_func.view_dataframe('test_files/', 'view_dataframe.csv', 'head', 5)
        expected_json = json.loads("""
        [ 
            {
                "a": 1,
                "b": 2,
                "c": 3
            }
        ]
        """
        )
        actual_json, expected_json = json.dumps(actual_json, sort_keys=True), json.dumps(expected_json, sort_keys=True)
        self.assertTrue(actual_json, expected_json)

    def test_remove_duplicates(self):
        actual_json = pandas_func.remove_duplicates('test_files/', 'remove_duplicates.csv', 'a')
        expected_json = json.loads("""
        [ 
            {
                "a": 1,
                "b": 2,
                "c": 3
            }
        ]
        """
        )
        actual_json, expected_json = json.dumps(actual_json, sort_keys=True), json.dumps(expected_json, sort_keys=True)
        self.assertTrue(actual_json, expected_json)

    #bro i dont get the requirements 💀
    def test_drop_null(self):
        print(pandas_func.remove_na('test_files', 'drop_null.csv', 'a'))

    #todo do assertions lol
    def test_replace_na_mean(self):
        print(pandas_func.replace_na_stat('test_files/', 'replace_na_mean.csv', 'a', 'mean'))

    #need a better test case for this...
    def test_replace_na_median(self):
        print(pandas_func.replace_na_stat('test_files/', 'replace_na_mean.csv', 'a', 'median'))

    def test_normalize_column(self):
        print(pandas_func.normalize_column('test_files', 'normalize_column.csv', 'a'))

if __name__ == '__main__':
    unittest.main()