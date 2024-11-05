#!/usr/bin/env python3

### sort.py sorts a specific playlist by artist's name

import spotipy
from spotipy.oauth2 import SpotifyOAuth
# from dotenv import load_dotenv
import argparse
import logging
import os

# load_dotenv()  # Load environment variables from .env

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load Spotify credentials from environment variables
# SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
# CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
# REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

print(f"Client ID: {os.getenv('SPOTIPY_CLIENT_ID')}")
print(f"Client Secret: {os.getenv('SPOTIPY_CLIENT_SECRET')}")
print(f"Redirect URI: {os.getenv('SPOTIPY_REDIRECT_URI')}")

# Authenticate with Spotify (one-time token)
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope="playlist-modify-public playlist-modify-private"))
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public playlist-modify-private"
))
# Retrieve the songs from the specified playlist
# Parameters:
# - playlist_id (str): the id of the Spotify playlist
# - user_id (str): the Spotify user id
# Returns:
# - song_list [Dict]: a list of dictionaries containing song details 
def get_playlist_tracks(playlist_id, user_id):
    # Try to get the tracks, if there's an error, throw that error to the user
    try:
        results = sp.user_playlist_tracks(user_id, playlist_id) # meta data and dictionary for all the tracks in the playlist
        tracks = results['items'] # array of SimplifiedPlaylistObject which represents a track in the playlist
        song_list = []

        while results['next']: # check url to the next page of items (null if none)
            results = sp.next(results) # get next page of results
            tracks.extend(results['items']) # add new times to the track list

        # extract specific details (stored in a dictionary) and append to song list
        for item in tracks:
            track = item['track']
            song_list.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'id': track['id']
            })
        return song_list

    except Exception as e:
        logging.error(f"Error retrieving tracks: {e}")
        return []

# Sort songs by artist name.
# Parameters:
# - songs [Dict]: a dictionary containing the tracks of a playlist
# Returns:
# - songs [Dict]: a sorted dictionary by artist name, all in lowercase characters
def sort_songs(songs):
    return sorted(songs, key=lambda x: x['artist'].lower())

# Update the specified playlist with sorted songs.
# Parameters:
# - playlist_id (str): Spotify ID of a specific playlist
# - sorted_songs [Dict]: sorted dictionary by artist name
# - user_id (str): A Spotify User ID
def update_playlist(playlist_id, sorted_songs, user_id):
    # Confirmation before update
    confirm = input("Are you sure you want to update the playlist? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Update canceled.")
        return
    
    else: 
        sp.user_playlist_replace_tracks(user_id, playlist_id, []) # replace existing track with an empty list
        song_ids = [song['id'] for song in sorted_songs] # create a list of song IDs from each ID in sorted_songs
        sp.user_playlist_add_tracks(user_id, playlist_id, song_ids) # adds list of track IDs in song_ids to the playlist in the given order
        logging.info(f"Updated playlist '{playlist_id}' with sorted songs.")

def main():
    # Check for environment variables
    if not SPOTIPY_CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
        raise ValueError("Missing Spotify credentials. Please check your .env file.")

    parser = argparse.ArgumentParser(description="Sort Spotify playlist by artist.")
    parser.add_argument("--playlist_id", required=True, help="The ID of the playlist to sort.")
    parser.add_argument("--user_id", required=True, help="The Spotify user ID.")
    
    args = parser.parse_args() # parse the arguments given by the command line
    playlist_id = args.playlist_id
    user_id = args.user_id

    songs = get_playlist_tracks(playlist_id, user_id)
    sorted_songs = sort_songs(songs)
    update_playlist(playlist_id, sorted_songs, user_id)

if __name__ == "__main__":
    main()
