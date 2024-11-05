import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public playlist-modify-private"))

def get_playlist_tracks(playlist_id):
    results = sp.user_playlist_tracks("vg3e1ffv9kaqgxq1sh5fr6kn4", playlist_id)
    tracks = results['items']
    song_list = []

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for item in tracks:
        track = item['track']
        song_list.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'id': track['id']
        })

    return song_list

def sort_songs(songs):
    return sorted(songs, key=lambda x: x['artist'].lower())

def update_playlist(playlist_id, sorted_songs):
    # Clear the playlist
    sp.user_playlist_replace_tracks("vg3e1ffv9kaqgxq1sh5fr6kn4", playlist_id, [])
    
    # Add sorted songs back to the playlist
    song_ids = [song['id'] for song in sorted_songs]
    sp.user_playlist_add_tracks("vg3e1ffv9kaqgxq1sh5fr6kn4", playlist_id, song_ids)

def main():
    playlist_id = "6Qo2NIZxTKipZDj3215oX6"

    songs = get_playlist_tracks(playlist_id)
    sorted_songs = sort_songs(songs)
    update_playlist(playlist_id, sorted_songs)

    print(f"Updated playlist '{playlist_id}' with sorted songs.")

if __name__ == "__main__":
    main()

