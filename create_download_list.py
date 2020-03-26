from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

scopes = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', scopes)
    creds = tools.run_flow(flow, store)
service = discovery.build('drive', 'v3', http=creds.authorize(Http()))

folder = 'application/vnd.google-apps.folder'
mimeType = 'mimeType'


def getFilesInFolder(folderId):
    response = service.files().list(q="'%s' in parents" % folderId,
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name, mimeType)',
                                    pageToken=pageToken).execute()

    return response.get('files', [])


pageToken = None

root = 'Enter folder ID here'

files = []
while True:
    response = service.files().list(q="'%s' in parents" % root,
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name, mimeType)',
                                    pageToken=pageToken).execute()
    for file in response.get('files', []):
        if file.get(mimeType) == folder:
            subFolderList = getFilesInFolder(file.get('id'))
            files.extend(subFolderList)
        else:
            files.append(file)
    pageToken = response.get('nextPageToken', None)
    if pageToken is None:
        break

with open("filesList.txt", 'w') as output:
    for file in files:
        output.write('%s (%s)' % (file.get('name'), file.get('id')) + '\n')
