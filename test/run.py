#!/usr/bin/python3

import requests

headers = {}

params = {}

host = "http://10.0.0.21"

result = requests.get(f"{host}", params=params, headers=headers)
print(result.text)
