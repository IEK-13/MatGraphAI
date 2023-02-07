import pandas as pd
import json
from flatten_json import flatten
f = open("./ror.json")

listi = []
def flatten_data(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

data = json.loads(f.read())
for el in data:
    add = flatten(el)
    listi.append(add)


df = pd.json_normalize(listi)
df.to_csv('institutions.csv')

