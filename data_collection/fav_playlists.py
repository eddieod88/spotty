from pandas import DataFrame
import spotipy.util

"""
Script to generate a csv of songs from a one of your Spotify Playlist.
Remember to export Spotify API access credentials to your session.
"""


def get_songs(chosen_playlist) -> []:
    """
        - Return a list of Songs from playlist.
    """
    songs = []
    tracks = chosen_playlist['tracks']
    while tracks:
        # gets groups of 100 tracks
        # loops through the group
        for i, item in enumerate(tracks['items']):
            song = item['track']
            songs.append(song)
        tracks = sp.next(tracks)
    return songs


username = 'dotdotdot123'
playlist_names = ['🛀  beats']
scope = 'user-library-read'
token = spotipy.util.prompt_for_user_token(username, scope)
if not token:
    print("Can't get token for {}".format(username))
    exit(1)

sp = spotipy.Spotify(auth=token)

playlist_ids = []
playlists = sp.user_playlists(username)
count = 0
while len(playlists['items']) > 0:
    count += 1
    for playlist in playlists['items']:
        print(playlist['name'])

        if any([playlist_name in playlist['name'].lower() for playlist_name in playlist_names]):
            print(playlist['id'])
            playlist_ids.append(playlist['id'])
    playlists = sp.user_playlists(username, offset=50*count)


playlists = [sp.playlist(playlist_id, fields="name,tracks,next") for playlist_id in playlist_ids]

songs = [(song, playlist['name']) for playlist in playlists for song in get_songs(playlist)]

print("Total songs found: {}".format(len(songs)))

# Then do gaussian model to split into <however many playlists have been used> groups. then try with new data.
audio = [
    {
        'artist': song['artists'][0]['name'],
        'name': song['name'],
        'playlist': playlist,
        'audio': sp.audio_features(song['id']),
    } for song, playlist in songs if song['id'] is not None
]


def convert_to_dataframe(data) -> DataFrame:
    df = DataFrame(data)
    df.insert(2, 'acousticness', [a[0].get('acousticness') for a in df.audio])
    df.insert(3, 'danceability', [a[0].get('danceability') for a in df.audio])
    df.insert(4, 'energy', [a[0].get('energy') for a in df.audio])
    df.insert(5, 'instrumentalness', [a[0].get('instrumentalness') for a in df.audio])
    df.insert(5, 'liveness', [a[0].get('liveness') for a in df.audio])
    df.insert(6, 'loudness', [a[0].get('loudness') for a in df.audio])
    df.insert(7, 'mode', [a[0].get('mode') for a in df.audio])
    df.insert(8, 'speechiness', [a[0].get('speechiness') for a in df.audio])
    df.insert(9, 'tempo', [a[0].get('tempo') for a in df.audio])
    df.insert(10, 'valence', [a[0].get('valence') for a in df.audio])
    df = df.drop(labels='audio', axis=1)
    return df

dataframe = convert_to_dataframe(audio)

# with open('songs.csv', 'w') as data_csv:
#     dataframe.to_csv(data_csv)
