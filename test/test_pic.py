#!/usr/bin/python3

import requests

headers = {}

params = {}

host = "http://10.0.0.21"

# content of test_class.py
class TestClass:
    def test_image(self):
        result = requests.get(f"{host}", params=params, headers=headers)
        image = result.content
        with open(f"test/test-image.jpg", "wb") as f:
            f.write(image)
            f.close()
