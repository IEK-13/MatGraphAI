import pandas as pd
import json
from flatten_json import flatten
f = open("./ror.json")

def flatten_data(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

data = json.loads(f.read())
data = flatten_data(data)
df = pd.json_normalize(data)
df.to_csv('institutions.csv')

