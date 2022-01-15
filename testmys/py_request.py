import json

import requests

data = {"user_list": [{"stu_name": "小飞"}]}
# data = json.dumps(data)

try:
    r = requests.post('http://localhost:50051/v1/User', json=data, headers={"Content-type": "application/json"})
    print(r.headers)
    print(r.content)
except requests.exceptions.ConnectionError as e:
    print(e)
    requests.status_code="Connection refused"
# print(r.text)
