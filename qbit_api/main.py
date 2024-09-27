import requests
import json
import time
import os
import threading
from datetime import datetime

# Set the URL of the qBittorrent WebUI
qb_url = 'http://192.168.1.15:8081/api/v2/auth/login'

seconds_CD = 60

# Set your credentials
credentials = {
    'username': 'admin',
    'password': 'adminadmin'
}

# File to store removed tracker information
removed_trackers_file = 'main.json'

# Dictionary to track torrents states
torrent_states = {}

# Load previously removed trackers from file

def read_removed_trackers_file(file_path):
    """
    Reads the JSON file and returns its contents as a list.
    If the file doesn't exist or is empty, returns an empty list.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

removed_trackers = read_removed_trackers_file(removed_trackers_file)

def write_removed_trackers_file(file_path, data):
    """
    Writes the data into the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_trackers(torrent, hash_string, downloading_torrents, retries=3):
    trackers_url = f'http://192.168.1.15:8081/api/v2/torrents/trackers?hash={hash_string}'
    for _ in range(retries):
        trackers_response = session.get(trackers_url)
        if trackers_response.status_code == 200:
            trackers = trackers_response.json()
            if trackers:
                tracker = trackers[-1]['url']
                if "**" in tracker:
                    print(f"{timestamp()} - ERROR tracker: {tracker}, name: {torrent['name']}, downloading_torrents : {downloading_torrents}")
                    raise ValueError(f"{tracker} isn't a valid tracker. You need to reassign manually the tracker of '{torrent['name']}'")
                return tracker
        time.sleep(1)  # Wait before retrying
    raise ValueError("Failed to get a valid tracker after multiple attempts.")


def start_download_and_remove_tracker(title, hash_string, tracker_to_remove, session):
    print(f"{timestamp()} - Download started for torrent: {title}")

    # Check if the torrent starts downloading
    check_state_url = f'http://192.168.1.15:8081/api/v2/torrents/info?hashes={hash_string}'
    timeout = 10  # Timeout in seconds
    interval = 0.5  # Check every 0.5 seconds
    elapsed = 0

    while elapsed < timeout:
        state_response = session.get(check_state_url)
        if state_response.status_code == 200:
            current_state = state_response.json()[0]['state']
            if current_state == 'downloading': # dès que le torrent passe en download, on retire le tracker

                # Store the torrent name and tracker URL
                removed_trackers.append({
                    'name': title,
                    'hash': hash_string,
                    'url': tracker_to_remove
                })

                # Remove the specified tracker
                remove_tracker_url = 'http://192.168.1.15:8081/api/v2/torrents/removeTrackers'
                data = {
                    'hash': hash_string,
                    'urls': tracker_to_remove
                }
                remove_response = session.post(remove_tracker_url, data=data)
                if remove_response.status_code == 200:
                    print(f"{timestamp()} - Tracker removed")
                else:
                    print(f"{timestamp()} - Failed to remove tracker, Error: {remove_response.status_code}")
                break

        time.sleep(interval)
        elapsed += interval

    if elapsed >= timeout:
        print(f"{timestamp()} - Timeout waiting for torrent {title} to start downloading.")

        # Stop the download since timeout exceeded
        pause_url = 'http://192.168.1.15:8081/api/v2/torrents/pause'
        pause_response = session.post(pause_url, data={'hashes': hash_string})
        if pause_response.status_code == 200:
            print(f"{timestamp()} - Torrent {title} has been paused due to timeout.")
        else:
            print(f"{timestamp()} - Failed to pause torrent {title}, Error: {pause_response.status_code}")

def reassign_tracker(hash_string, title, tracker_to_add):
    """
    Pauses the torrent, reassigns the tracker, and resumes the torrent.

    Args:
        session: The current requests.Session object.
        hash_string: The hash of the torrent.
        title: The name of the torrent.
        tracker_to_add: The tracker URL to be reassigned.
    """
    torrents_url = 'http://192.168.1.15:8081/api/v2/torrents/info'

    # Pause the torrent
    pause_url = 'http://192.168.1.15:8081/api/v2/torrents/pause'
    pause_response = session.post(pause_url, data={'hashes': hash_string})

    if pause_response.status_code == 200:
        print(f"{timestamp()} - Paused torrent: {title}")
    else:
        print(f"{timestamp()} - Failed to pause torrent: {title}, Error: {pause_response.status_code}")
        return False

    # Wait until the torrent is confirmed to be in a paused state
    while True:
        torrent_info = session.get(torrents_url).json()
        current_state = next(
            (t['state'] for t in torrent_info if t['hash'] == hash_string), None
        )
        if current_state == 'pausedUP':
            print(f"{timestamp()} - Torrent {title} is now paused.")
            break
        time.sleep(0.5)  # Check frequently

    # Reassign the tracker
    add_tracker_url = 'http://192.168.1.15:8081/api/v2/torrents/addTrackers'
    data = {
        'hash': hash_string,
        'urls': tracker_to_add
    }
    add_response = session.post(add_tracker_url, data=data)

    if add_response.status_code == 200:
        print(f"{timestamp()} - Tracker added back to torrent: {title}")

        # Resume the torrent
        resume_url = 'http://192.168.1.15:8081/api/v2/torrents/resume'
        resume_response = session.post(resume_url, data={'hashes': hash_string})

        if resume_response.status_code == 200:
            print(f"{timestamp()} - Resumed torrent: {title}")
            return True
        else:
            print(f"{timestamp()} - Failed to resume torrent: {title}, Error: {resume_response.status_code}")
            return False
    else:
        print(f"{timestamp()} - Failed to add tracker back to torrent: {title}, Error: {add_response.status_code}")
        return False

def resume_torrent(session, hash_string):
    """Resume a paused torrent based on its hash.

    Args:
        session (requests.Session): The session object for making HTTP requests.
        hash_string (str): The hash of the torrent to resume.

    Returns:
        bool: True if the resume request was successful, False otherwise.
    """
    resume_url = 'http://192.168.1.15:8081/api/v2/torrents/resume'
    try:
        # Sending hash string in the body
        response = session.post(resume_url, data={'hashes': hash_string})
        if response.status_code == 200:
            print(f"{timestamp()} - Successfully resumed torrent with hash {hash_string}")
            return True
        else:
            print(f"{timestamp()} - Failed to resume torrent with hash {hash_string[:10]}, Error: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"{timestamp()} - Exception occurred while resuming torrent with hash {hash_string[:10]}: {e}")
        return False

def monitor_torrents():
    downloading_torrents = {}
    unpaused_torrents = []
    max_unpause_count = 3  # Define how many torrents to unpause at a time
    max_active_torrents = 3  # Define the maximum number of active torrents allowed before unpausing more (with DOWNLADING state)
    unpaused_count = 0
    counter_cpt = 0

    while True:
        counter_cpt += 1
        torrents_url = 'http://192.168.1.15:8081/api/v2/torrents/info?filter=active'
        torrents_url_paused = 'http://192.168.1.15:8081/api/v2/torrents/info?filter=paused'
        
        response = session.get(torrents_url)
        response_paused = session.get(torrents_url_paused)

        # Check the state of unpaused torrents
        for hash_string in unpaused_torrents[:]:
            check_state_url = f'http://192.168.1.15:8081/api/v2/torrents/info?hashes={hash_string}'
            state_response = session.get(check_state_url)
            if state_response.status_code == 200:
                current_state = state_response.json()[0]['state']
                if current_state in ["uploading", "stalledUP", "pausedUP"]:
                    # Torrent has moved out of the downloading state
                    unpaused_torrents.remove(hash_string)
                    # del downloading_torrents[hash_string]
                    unpaused_count -= 1
                    print(f"{timestamp()} - Torrent with hash {hash_string[:10]} is no longer downloading. {unpaused_count} been decreased")


        response = session.get(torrents_url)
        
        if response.status_code == 200:
            torrents = response.json()
            active_count = 0  # Number of active torrents with the state DOWNLOADING
            for torrent in torrents:
                state = torrent['state']
                if state == "downloading":
                    active_count += 1

        # Check paused torrents
        if response_paused.status_code == 200:
            torrents_paused = response_paused.json()
            
            # Unpause a limited number of torrents if the active torrent count is below the limit
            # print()
            # print(timestamp(), " - ", "active_count < max_active_torrents = ",  active_count < max_active_torrents)

            if active_count < max_active_torrents:
                
                for torrent in torrents_paused:
                    state = torrent['state']
                    title = torrent['name']
                    hash_string = torrent['hash']
                    if state == "pausedDL" and unpaused_count < max_unpause_count:
                        print(f"{timestamp()} - Attempting to unpause Title : {title} | State : {state}")
                        if resume_torrent(session, hash_string):
                            unpaused_count += 1
                            unpaused_torrents.append(hash_string)
                    if unpaused_count == max_unpause_count:
                        break
                # print(timestamp(), " - ", "END CHECK paused torrent")



        response = session.get(torrents_url)

        if response.status_code == 200:
            torrents = response.json()

            for torrent in torrents:
                title = torrent['name']
                hash_string = torrent['hash']
                state = torrent['state']
                if state == "downloading":
                    if hash_string not in downloading_torrents:
                        tracker = get_trackers(torrent, hash_string, downloading_torrents)
                        print(f"{timestamp()} - Title : {title} | State : {state} | Trackers : {tracker} (start DL)")
                        start_download_and_remove_tracker(title, hash_string, tracker, session)
                        write_removed_trackers_file(removed_trackers_file, removed_trackers)
                        downloading_torrents[hash_string] = tracker

        keys_to_delete = []

        # Check torrents that are already downloading to see if they are now seeding
        for hash_string, tracker in downloading_torrents.items():
            check_state_url = f'http://192.168.1.15:8081/api/v2/torrents/info?hashes={hash_string}'
            state_response = session.get(check_state_url)
            
            if state_response.status_code == 200:
                current_state = state_response.json()[0]['state']
                
                if current_state in ["uploading", "stalledUP", "pausedUP"]:
                    title = state_response.json()[0]['name']
                    print(f"{timestamp()} - Torrent '{title}' is now seeding {hash_string[:10]}... . Reassigning {tracker}.")

                    reassign_tracker(hash_string, title, tracker)
                    keys_to_delete.append(hash_string)  # Mark the key for deletion

        # Remove marked keys from the dictionary outside of the loop
        for key in keys_to_delete:
            del downloading_torrents[key]

        if counter_cpt % 800 == 0:
            print("======"*10)
            print(f"{timestamp()} - downloading_torrents SIZE = {len(downloading_torrents)}")
            print(f"{timestamp()} - removed_trackers SIZE     = {len(removed_trackers)}")
            print(f"{timestamp()} - unpaused_torrents SIZE    = {len(unpaused_torrents)}")
            print("_____"*5)
            print("downloading_torrents = ", downloading_torrents)
            print("_____"*5)
            print("unpaused_torrents = ", unpaused_torrents)
            print("======"*10)
            counter_cpt = 0
        # print(timestamp(), " - ", "WHILE restart")
        time.sleep(10)  # Check every seconds

        # print(removed_trackers)


def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    # Keep the main thread running to allow for interruptions
    try:
        while True:
            # Authenticate and get the session cookie
            try:
                session = requests.Session()
                response = session.post(qb_url, data=credentials)
                response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
            except Exception as e:
                print(f"{timestamp()} - FAILED TO CONNECT TO THE SERVICE: {e}")
                time.sleep(seconds_CD)  # Wait for the specified time before retrying
                continue  # Retry the connection

            # Check if authentication was successful
            print(f"{timestamp()} - Authenticated successfully")
            print(f"{timestamp()} ------------------ START - monitor_torrents() ------------------")
            monitor_torrents()
            print(f"{timestamp()} ------------------ END - monitor_torrents() ------------------")
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"{timestamp()} - Script interrupted and will be ended.")
