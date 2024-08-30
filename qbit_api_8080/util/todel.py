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

# List of torrent hashes you want to pause and add tracker
# torrent_hashes = [
# "b7088fb86b723a9cacb8ac3aed82f8c7dc901b14",
# "ac37e4175a196503a1791b78f0330cfc0868b27d",
# "213dc87522d686e6de7c32ab480c21d1a9e73abb",
# "bb82c547515a25a04d3216011480cb7dd47d27e7",
# "da01706928eeb90f5763bfae560caf6a44d36cff",
# "af7f7b0a27feb442c88ffbd17cbb1b6d66e6983a"
# ]

# torrent_hashes = ["b7088fb86b723a9cacb8ac3aed82f8c7dc901b14",
# "ac37e4175a196503a1791b78f0330cfc0868b27d"]


torrent_hashes = ['4bfd47424dedba464e82ffc5b0cafcd8b4c3fc80',
'af7f7b0a27feb442c88ffbd17cbb1b6d66e6983a','b7088fb86b723a9cacb8ac3aed82f8c7dc901b14']

# Tracker to add
tracker_url = 'https://www.sharewood.tv/announce/1dd21a005b8e22df1e0a15a90805a41c'

# Pause torrents and add tracker
for hash_string in torrent_hashes:
    # Pause the torrent
    pause_url = qb_url + 'torrents/pause'
    pause_response = session.post(pause_url, data={'hashes': hash_string})

    if pause_response.status_code == 200:
        print(f"Paused torrent: {hash_string}")
    else:
        print(f"Failed to pause torrent: {hash_string}, Error: {pause_response.status_code}")
        continue

    # Add the tracker to the paused torrent
    add_tracker_url = qb_url + 'torrents/addTrackers'
    data = {
        'hash': hash_string,
        'urls': tracker_url
    }
    add_response = session.post(add_tracker_url, data=data)

    if add_response.status_code == 200:
        print(f"Tracker added to torrent: {hash_string}")
    else:
        print(f"Failed to add tracker to torrent: {hash_string}, Error: {add_response.status_code}")


# Directory to be cleaned
incomplete_downloads_dir = '/media/diego/downloads/incomplete'

# Remove all contents of the directory without deleting the folder itself
for filename in os.listdir(incomplete_downloads_dir):
    file_path = os.path.join(incomplete_downloads_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        print(f"Removed: {file_path}")
    except Exception as e:
        print(f"Failed to delete {file_path}. Reason: {e}")


# Force recheck on the specified torrents
for hash_string in torrent_hashes:
    recheck_url = qb_url + 'torrents/recheck'
    recheck_response = session.post(recheck_url, data={'hashes': hash_string})

    if recheck_response.status_code == 200:
        print(f"Recheck initiated for torrent: {hash_string}")
    else:
        print(f"Failed to initiate recheck for torrent: {hash_string}, Error: {recheck_response.status_code}")


# Force recheck on the specified torrents
for hash_string in torrent_hashes:
    # Recheck the torrent
    recheck_url = qb_url + 'torrents/recheck'
    recheck_response = session.post(recheck_url, data={'hashes': hash_string})

    if recheck_response.status_code == 200:
        print(f"Recheck initiated for torrent: {hash_string}")
    else:
        print(f"Failed to initiate recheck for torrent: {hash_string}, Error: {recheck_response.status_code}")
    
    # Force reannounce to the tracker
    reannounce_url = qb_url + 'torrents/reannounce'
    reannounce_response = session.post(reannounce_url, data={'hashes': hash_string})

    if reannounce_response.status_code == 200:
        print(f"Reannounce initiated for torrent: {hash_string}")
    else:
        print(f"Failed to initiate reannounce for torrent: {hash_string}, Error: {reannounce_response.status_code}")
