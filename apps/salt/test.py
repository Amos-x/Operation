from salt import settings
import requests
import json

_url = settings.SALT_API_URL
_username = settings.SALT_USER
_passwd = settings.SALT_PASSWD
headers = {'Content-Type': 'application/json'}
data = {
    'eauth': 'pam',
    'username': _username,
    'password': _passwd,
}
login_url = '%s%s' % (_url, '/login')

response = requests.post(login_url, data=json.dumps(data), headers=headers, verify=False)
token = response.json()['return'][0]['token']
print(response.json())
