import json
import requests

username = 'demouser'
password = 'demouser'
hub_url = 'http://127.0.0.1:443'

login_url = hub_url + '/hub/login'
token_url = hub_url + '/hub/api/authorizations/token'

# step 1: login with username + password
r = requests.post(login_url, data={'username': username, 'password': password}, allow_redirects=False)
r.raise_for_status()
cookies = r.cookies

# 2. request token
r = requests.post(token_url,
    headers={'Referer': login_url},
    cookies=cookies,
)
r.raise_for_status()
token = r.json()['token']

auth_headers = {'Authorization': 'token %s' % token}

# 3. check if running, spawn if not
url = None
while url is None:
    r = requests.get(hub_url + '/hub/api/users/%s' % username, headers=auth_headers)
    r.raise_for_status()
    status = r.json()
    url = status['server']
    if not url and not status['pending']:
        r = requests.post(hub_url + '/hub/api/users/%s/server' % username, headers=auth_headers)
        r.raise_for_status()
