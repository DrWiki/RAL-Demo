#!/usr/bin/python
import json

jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}';

text = json.loads(jsonData)
print(text)
print(text["a"])
print(text["b"])
print(text["c"])
print(text["d"])
print(text["e"])
