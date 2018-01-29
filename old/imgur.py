import base64
import requests
import json

from base64 import b64encode

client_id = ''

headers = {"Authorization": "Client-ID " + client_id}

url = "https://api.imgur.com/3/upload.json"

resp = requests.post(
    url, 
    headers = headers,
    data = {
        'image': b64encode(open('1.jpg', 'rb').read()),
        'type': 'base64',
        'name': '1.jpg',
        'title': 'Picture no. 1'
    }
)

json_resp = json.loads(resp.text)
print(json_resp['data']['link'])
