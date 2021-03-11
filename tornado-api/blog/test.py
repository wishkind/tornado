import requests


res = requests.get('http://localhost:9999/api/v1/tag')
res = requests.get('http://localhost:8888/api/v1/tag')

print(res.text)
