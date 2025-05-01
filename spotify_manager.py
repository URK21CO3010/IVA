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
    scope="playlist-modify-public playlist-read-private playlist-modify-private",
    username=USERNAME
))

def create_playlist(playlist_name):
    playlist = sp.user_playlist_create(user=USERNAME, name=playlist_name, public=True)
    print(f"Created playlist '{playlist_name}'")
    return playlist["id"]

def add_songs_to_playlist(playlist_name, song_names):
    # Find playlist by name
    playlists = sp.current_user_playlists()
    playlist_id = None
    for item in playlists["items"]:
        if item["name"] == playlist_name:
            playlist_id = item["id"]
            break

    if not playlist_id:
        print(f"Playlist '{playlist_name}' not found.")
        return

    track_uris = []
    for name in song_names:
        result = sp.search(q=name, type="track", limit=1)
        items = result["tracks"]["items"]
        print(name, '->', end = ' ')
        for i in items:
            print(i['name'])
        if items:
            track_uris.append(items[0]["uri"])
        else:
            print(f"Song '{name}' not found.")

    if track_uris:
        sp.playlist_add_items(playlist_id, track_uris)
        print(f"Added {len(track_uris)} songs to playlist '{playlist_name}'")

def delete_playlist(playlist_name):
    playlists = sp.current_user_playlists()
    for playlist in playlists["items"]:
        if playlist["name"] == playlist_name:
            sp.current_user_unfollow_playlist(playlist["id"])
            print(f"Deleted playlist '{playlist_name}'")
            return
    print(f"Playlist '{playlist_name}' not found.")
