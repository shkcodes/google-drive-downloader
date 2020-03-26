# google-drive-downloader
Batch files from Google Drive

## How To Use
1) Setup Python on your system
2) Create a new [Google Drive project](https://developers.google.com/drive/activity/v1/guides/project)
3) Create an OAuth 2 Client ID from [here](https://console.developers.google.com/apis/credentials) and download the resulting json file. Rename it to  `client_secret.json`
4) Move both the scripts from this repo and the downloaded json file to a single directory
5) Open `create_download_list.py` and replace `Enter folder ID here` with the folder ID you want to download
6) Save and run `create_download_list.py`
7) This will create a `filesList.txt` in your current directory. You can modify this file to remove the files you don't want to download
8) Run `download_files.py` and wait for the download to complete!
