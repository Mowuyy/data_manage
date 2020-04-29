# -*- coding: utf-8 -*-

import json

test_map = {"a": 5, "b": 3}

data = [3, 4, 4, 5, 5, 5]

item = [3, 4, 3, 43, 56]

# data.pop(0)
# print(data)

del data[0], data[2:], item[0]
print(data)
print(item)

