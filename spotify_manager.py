import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
CLIENT_ID = "f60ae9a7a5ae41ca97f8b1f71c56d507"
CLIENT_SECRET = "57dd8ed4d03546c68d475be06688729c"
REDIRECT_URI = "http://localhost:3000"
USERNAME = "31ey5nt6mvzki4oo6kcxgq5auf6i"

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-public",
    username=USERNAME
))

# Function to search for tracks
def search_tracks(keyword, limit=1):
    results = sp.search(q=keyword, type="track", limit=limit)
    track_uris = [track["uri"] for track in results["tracks"]["items"]]
    return track_uris

# Function to create a playlist
def create_playlist(name, description=""):
    playlist = sp.user_playlist_create(user=USERNAME, name=name, public=True, description=description)
    return playlist["id"]

# Function to add tracks to a playlist
def add_tracks_to_playlist(playlist_id, track_uris):
    sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)

def get_playlist_id(playlist_name):
    for playlist in sp.user_playlists(USERNAME)['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']

def delete_playlist(playlist_id):

    sp.current_user_unfollow_playlist(playlist_id)
