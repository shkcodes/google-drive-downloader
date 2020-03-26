import io

from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools

scopes = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', scopes)
    creds = tools.run_flow(flow, store)
service = discovery.build('drive', 'v3', http=creds.authorize(Http()))

with open('filesList.txt') as f:
    items = f.read().splitlines()

fileIds = list(map(lambda item: item[item.find("(") + 1:item.find(")")], items))

downloadFolderMeta = {
    'name': 'TBD',
    'mimeType': 'application/vnd.google-apps.folder'
}

downloadFolder = service.files().create(body=downloadFolderMeta,
                                        fields='id').execute().get('id')

body = {'parents': [downloadFolder]}
copiedFiles = []

for fileId in fileIds:
    copiedFile = service.files().copy(fileId=fileId, body=body).execute()
    copiedFileId = copiedFile.get('id')
    copiedFileName = copiedFile.get('name')
    request = service.files().get_media(fileId=copiedFileId)
    fh = io.FileIO(copiedFileName, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Downloading %s %d%%" % (copiedFileName, int(status.progress() * 100)))
    print("Downloaded %s" % copiedFileName)
    service.files().delete(fileId=copiedFileId).execute()
