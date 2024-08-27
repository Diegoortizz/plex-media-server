import requests
import shutil
import os

# Set the URL of the qBittorrent WebUI
qb_url = 'http://192.168.1.15:8081/api/v2/'

# Set your credentials
credentials = {
    'username': 'admin',
    'password': 'adminadmin'
}

# Authenticate and get the session cookie
session = requests.Session()
response = session.post(qb_url + 'auth/login', data=credentials)

# Check if authentication was successful
if response.text == 'Ok.':
    print('Authenticated successfully')
else:
    print('Failed to authenticate:', response.text)
    exit()


torrents_url = 'http://192.168.1.15:8081/api/v2/torrents/info?filter=downloading'

response = session.get(torrents_url)

if response.status_code == 200:
    torrents = response.json()
    for torrent in torrents:
        state = torrent['state']
        print(torrent["name"], state)