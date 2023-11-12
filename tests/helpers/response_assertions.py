import json
import os
from pathlib import Path

def expected_response_data_for(filepath, response):
    filepath += 'response.data.json'

    Path(os.path.dirname(filepath)).mkdir(parents=True, exist_ok=True)

    if (os.path.isfile(filepath)):
        with open(filepath) as file:
            data = json.load(file)

    else:
        with open(filepath, 'w+') as file:
            data = json.loads(response.data.decode('utf8'))
            json.dump(data, file, indent=2)
    
    return data

def assert_data(path, response):
    actual = json.loads(response.data.decode('utf8'))
    expected = expected_response_data_for(path, response)

    assert json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
