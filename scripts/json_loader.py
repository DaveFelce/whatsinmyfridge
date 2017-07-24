from os import listdir
from os.path import isfile, join
import json
import requests

if __name__ == '__main__':

    path = '../fixtures'
    json_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    for json_file in json_files:
        print("DOING FILE: " + json_file)
        with open(json_file) as f:
            data = json.load(f)

        for row_dict in data:
            print("doing " + json.dumps(row_dict))
            url = 'http://localhost/recipes/list/'
            r = requests.post(url, json=row_dict)
            print(r.status_code)



