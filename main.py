import json

import requests

from pipeline.utils.utils import Utils

app_key = "7yiemxlek5s846k"
app_secret = "g70t3hljceheq04"

# build the authorization URL:
authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key

# send the user to the authorization URL:

print(authorization_url)

# get the authorization code from the user:
authorization_code = input('Enter the code:\n')

# exchange the authorization code for an access token:
token_url = "https://api.dropboxapi.com/oauth2/token"
params = {
    "code": authorization_code,
    "grant_type": "authorization_code",
    "client_id": app_key,
    "client_secret": app_secret
}
r = requests.post(token_url, data=params)
print(r.text)
res = json.loads(r.text)
print(type(res))
Utils().saveObject(res['access_token'], "data/credentials/acces_token.pickle")
