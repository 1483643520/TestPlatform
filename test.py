#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# test.py
# 
# author:zhaohexin
# time：2020/4/1 18:30

import json

# str = '{"name":"TRUE","Gender":"male","age":23}'

str = '{"details":[{"success": "False", "stat": {"total": 2,' \
      ' "failures": 0, "errors": 1, "skipped": 0, "expectedFailures": 0, "unexpectedSuccesses": 0, "successes": 1}]}'
js = json.loads(str)
print(js)
