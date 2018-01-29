
import dropbox

token = ""
dbx = dropbox.Dropbox(token)

fullname = '../0.jpg'
with open(fullname, 'rb') as f:
    data = f.read()
result = dbx.files_upload(data, '/ticketing/0.jpg', mode = dropbox.files.WriteMode.add, autorename = True)

upload_path = result.path_display

result = dbx.sharing_create_shared_link(upload_path, short_url=False)
url = result.url.replace('www.dropbox.com', 'dl.dropboxusercontent.com')
print(url)
