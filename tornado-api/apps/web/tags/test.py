import requests


res = requests.get('http://127.0.0.1:9999/api/v2/tag/get', json={'hot': 'true'})


print(res.text)
