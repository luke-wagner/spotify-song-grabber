from SwSpotify import spotify
import spotipy
import spotipy.util as util
from song_grabber_config import CLIENT_ID, CLIENT_SECRET, USERNAME, SCOPE, REDIRECT_URI, PLAYLIST_ID

#Get token
print("Retrieving user token...")
token = util.prompt_for_user_token(
    username=USERNAME,
    scope=SCOPE,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI
)

#Instantiate object
print("Creating spotipy obj...")
sp = spotipy.Spotify(auth=token)

#Get song name and artist name
print("Getting song info...")
try:
    song = spotify.song()
    artist = spotify.artist()
except:
    print("--No song found")
    quit()

#Define query
print("Defining search query...")
q = song + " artist:" + artist

#Get song id
print("Retrieving query[0] id...")
try:
    song_id = str(sp.search(q, limit=1, type="track")["tracks"]["items"][0]["id"])
    print("--song_id: " + song_id)
except:
    print("--Retrieval failed.")
    exit()

#Check if playlist contains song
print("Checking for duplicates...")
playlist_items = sp.playlist_items(PLAYLIST_ID)
for item in playlist_items["items"]:
    if song_id == item["track"]["id"]:
        print("--Duplicate found.")
        exit()

#Add to playlist
print("Adding song to playlist...")
sp.playlist_add_items(PLAYLIST_ID, [song_id])
print("--Done!")
