# https://stackoverflow.com/questions/38633791/python-request-post-images-on-facebook-using-multipart-form-data
import requests
import json

access_token = ""

data = {
    #'caption': "test upload",
    'access_token': access_token,
	'published': 'false'
}

files = {
    'file': open('0.jpg', 'rb')
}
resp = requests.post(
    'https://graph.facebook.com/v2.11/me/photos',
     data=data, files=files)
json_resp = json.loads(resp.text)
id_0 = json_resp['id']


files = {
    'file': open('1.jpg', 'rb')
}
resp = requests.post(
    'https://graph.facebook.com/v2.11/me/photos',
     data=data, files=files)
json_resp = json.loads(resp.text)
id_1 = json_resp['id']

data = {
    'message': "test upload",
	'attached_media[0]' : '{"media_fbid":"%s"}' % id_0,
	'attached_media[1]' : '{"media_fbid":"%s"}' % id_1,
    'access_token': access_token,
}
resp = requests.post(
    'https://graph.facebook.com/v2.11/me/feed',
     data=data)
