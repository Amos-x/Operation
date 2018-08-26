from django.test import TestCase
# Create your tests here.
import json
import requests

token = '0378211d367f6e6abb6957265dbdd9299b2fbfe3'

headers = {
    'X-Auth-Token':token,
    'Content-Type': 'application/json',
}
data = {
    'client': 'local',
    'tgt': ['192.168.9.54'],
    'fun': 'cmd.run',
    'arg': "fdisk -l |sed -n '2p'",
    'expr_form': 'list',
}
url = 'https://192.168.9.89:8000'
response = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
print(response.json())
if not response.json()['return'][0]:
    print('ok')