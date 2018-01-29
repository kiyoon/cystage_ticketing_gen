#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI
import io
import getpass
import os

"""
## Uploading a timeline album (aka carousel aka sidecar).
"""
media = [  # Albums can contain between 2 and 10 photos/videos.
    {
        'type': 'photo',
        'file': '0.jpg',  # Path to the photo file.
    },
]

# find jpg files and add to album
file_index = 1
file_to_add = '%d.jpg' % file_index
while os.path.isfile(file_to_add):
	media.append({'type':'photo', 'file': file_to_add})
	file_index += 1
	file_to_add = '%d.jpg' % file_index

with io.open('sns_caption.txt','r',encoding='utf8') as f:
    captionText = f.read()
userid = "test"
print()
print("User ID: " + userid)
password = getpass.getpass()
ig = InstagramAPI(userid, password)
ig.login()
ig.uploadAlbum(media, caption=captionText)
