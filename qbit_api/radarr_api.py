import time
import requests
from datetime import datetime
import sys


def is_radarr_up(radarr_api_url):
    try:
        response = requests.get(f"{radarr_api_url}/api/v3/system/status", params={'apikey': "8b17c42c6bb94e15bac07e5d1c325f49"})
        return response.status_code == 200
    except requests.exceptions.RequestException:
        sys.exit(1)
        return False

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_all_movies_from_radarr(api_url, api_key):
    headers = {
        'X-Api-Key': api_key
    }
    response = requests.get(f'{api_url}/api/v3/movie', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{timestamp()} - Failed to retrieve movies from Radarr. Status code: {response.status_code}")
        return None

def delete_and_blocklist_movie_in_radarr(movie_id, api_url, api_key, title, delete_files=False, add_import_exclusion=True):
    headers = {
        'X-Api-Key': api_key
    }
    # Construct the query parameters based on the function arguments
    query_params = {
        'deleteFiles': str(delete_files).lower(),
        'addImportExclusion': str(add_import_exclusion).lower()
    }
    response = requests.delete(f'{api_url}/api/v3/movie/{movie_id}', headers=headers, params=query_params)
    
    if response.status_code == 200:
        print(f"{timestamp()} - Successfully deleted <{title}> ({movie_id}).")
    else:
        print(f"{timestamp()} - Failed to delete movie  <{title}> ({movie_id}). Status code: {response.status_code}, Response: {response.text}")

def load_exceptions(file_path):
    """Load the list of exceptions from a text file."""
    try:
        with open(file_path, 'r') as file:
            exceptions = {line.strip().lower() for line in file.readlines()}
        return exceptions
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. No exceptions will be applied.")
        sys.exit(1)
        return set()

def get_tag_id_by_label(api_url, api_key, label):
    headers = {
        'X-Api-Key': api_key
    }
    response = requests.get(f'{api_url}/api/v3/tag', headers=headers)
    
    if response.status_code == 200:
        tags = response.json()
        for tag in tags:
            if tag['label'] == label:
                return tag['id']
    print(f"{timestamp()} - Tag with label '{label}' not found.")
    sys.exit(1)
    raise ValueError(f"Couldn't find overseerr tag.")


def main_radarr_api():

    print(f"{timestamp()} ---- START - radarr_api() ----")

    # Replace these with your actual Radarr API URL and key
    radarr_api_url = "http://localhost:7879"
    radarr_api_key = "8b17c42c6bb94e15bac07e5d1c325f49"


    # Check if Radarr is available
    if not is_radarr_up(radarr_api_url):
        print(f"{timestamp()} - Radarr is not up, skipping this run.")
        sys.exit(1)


    # Set a minimum rating threshold
    rating_threshold = 6.5  # Only keep movies with a rating of 6.5 or higher

    # Load exceptions from file
    exceptions_file_path = '/home/diego/htpc-download-box/radarr_api/exceptions.txt'
    exceptions = load_exceptions(exceptions_file_path)

    overseer_tag_id = get_tag_id_by_label(radarr_api_url, radarr_api_key, "overseerr")

    # Fetch all movies from Radarr
    movies = get_all_movies_from_radarr(radarr_api_url, radarr_api_key)


    for movie in movies:
        title = movie['title']
        alt_title = movie["originalTitle"]


        # Skip if the movie title is in the exceptions list
        if any(exc in title.lower() for exc in exceptions) or any(exc in alt_title.lower() for exc in exceptions):
            # print(f"{timestamp()} - <{title}> SKIPPED (exceptions list)")
            continue
        
        if (overseer_tag_id in movie["tags"]): # 13 being the watchlist's tags
            # print(f"{timestamp()} - <{title}> SKIPPED (watchlist)")
            continue

        if 'imdb' not in movie['ratings']: # movie isn't released yet (ie no ratings)
            continue
        

        imdb_rating = movie['ratings']['imdb']['value']
        movie_id = movie['id']  # Radarr movie ID
        movie_genres = movie['genres']

        if movie["originalLanguage"]["name"] == "Telugu":
            print(f"{timestamp()} - {title} DELETED ({imdb_rating}/10) (INDIEN)")
            delete_and_blocklist_movie_in_radarr(movie_id, radarr_api_url, radarr_api_key, title, delete_files=True, add_import_exclusion=True)

        if any(genre in ["Family", "Animation"] for genre in movie_genres):
            print(f"{timestamp()} - {title} DELETED ({imdb_rating}/10) ({movie['genres']})")
            delete_and_blocklist_movie_in_radarr(movie_id, radarr_api_url, radarr_api_key, title, delete_files=True, add_import_exclusion=True)
            continue

        if any(genre in ["Horror"] for genre in movie_genres) and imdb_rating < 8:
            print(f"{timestamp()} - {title} DELETED ({imdb_rating}/10) ({movie['genres']})")
            delete_and_blocklist_movie_in_radarr(movie_id, radarr_api_url, radarr_api_key, title, delete_files=True, add_import_exclusion=True)
            continue

    print(f"{timestamp()} ---- END - radarr_api() ----")


while True:
    main_radarr_api()
    time.sleep(60)  # Wait for 60 seconds before running again