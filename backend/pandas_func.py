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