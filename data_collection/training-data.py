import sqlite3
import argparse
import pprint
from random import shuffle


import spotipy
import spotipy.util

"""
    Program which interactively allows the user to tag songs in their spotify playlists. Information stored on a db.

    Walkthrough:
    1 - Open Database - program argument is the name of the path. (if it doesn't exist, it will create a new one with a provided schema.)
    2 - Select a Playlist of which to tag up.
    3 - Loop
        3.1 - Present user with song (possibly play a clip of it)
        3.2 - Ask user to type in a tag for it - just one for now. Type 'q' to exist loop
        3.3 - If tag doesn't exist, ask if user wants to create a new one
        3.4 - Enter into db. (Song metadata, musical data, tag)

    Features:
     - Quit at any time and save changes

    Notes:
     - Remember to start up a local host server and export the Spotify API credentials

    TODO:
     - Safety feature if you miss spell a tag
     - AWS RDS
     - Choose playlist from program arg
"""


def get_songs(conn, chosen_playlist) -> []:
    """
        - Return a list of Songs in any order. 
        - Only include songs which are not in the db. 
    """
    songs = []
    c = conn.cursor()
    
    tracks = chosen_playlist['tracks']
    while tracks['next']:
        # gets groups of 100 tracks
        tracks = sp.next(tracks)
        # loops through the group
        for i, item in enumerate(tracks['items']):
            song = item['track']
            metadata = (song['name'], song['artists'][0]['name'], song['album']['name'], )
            c.execute("SELECT _id FROM Song WHERE Title=? AND Artist=? AND Album=?;", metadata)
            song_exists = c.fetchone()
            if not song_exists and song['id'] is not None:
                songs.append(song)

    shuffle(songs)
    return songs
        
def create_db(conn):
    with open('songs_db_script.sql', 'r') as sql_script:
        s = sql_script.read()
        cur = conn.cursor()
        cur.executescript("""{}""".format(s))

def insert_to_db(conn, song, charateristics, tag):
    chars = charateristics[0]
    c = conn.cursor()
    tag = tag.lower()
    tag_insert = (tag, )
    song_insert = (song['name'], song['artists'][0]['name'], song['album']['name'], chars['acousticness'],
                chars['danceability'], chars['energy'], chars['instrumentalness'], chars['key'], chars['liveness'],
                chars['speechiness'], chars['tempo'], chars['valence'], )
    try:
        c.execute("INSERT INTO Tag (Name) VALUES (?)", tag_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    try:
        c.execute("INSERT INTO Song (Title, Artist, Album, Acousticness, Danceability, Energy, Instrumentalness, MusicalKey, Liveness, Speechiness, Tempo, Valence)" \
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", song_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    relationship_insert = (song['name'], song['artists'][0]['name'], song['album']['name'], tag,)
    c.execute("INSERT INTO Relationship (Song_id, Tag_id) VALUES ((SELECT _id FROM Song WHERE Title=? AND Artist=? AND Album=?), (SELECT _id FROM Tag WHERE Name=?));", relationship_insert)
    conn.commit()

def check_tag_exists(tag):
    pass


parser = argparse.ArgumentParser(description="Tag up some songs")
parser.add_argument('db_path', metavar='db_path', type=str, help="relative db path destination from top dir")
parser.add_argument('username', metavar='spotify_user',type=str, help="Username of desired Spotify account")
parser.add_argument('--reset-db', action='store_true', help="Option to recreate the database from scratch - Use this on first time use too")
args = parser.parse_args()

username = args.username
the_vibe_id = '51p6p68CssRUi23lCWD78z'

scope = 'user-library-read'
token = spotipy.util.prompt_for_user_token(username, scope)

if not token:
    print("Can't get token for {}".format(username))
    exit(1)
sp = spotipy.Spotify(auth=token)
playlist = sp.user_playlist(username, playlist_id=the_vibe_id, fields="tracks,next")

db_conn = sqlite3.connect('training_songs.db')
if args.reset_db:
    create_db(db_conn)

songs = get_songs(db_conn, playlist)
# pprint.pprint(songs)

print("Total songs found: {}".format(len(songs)))

print("Type some tags which you would like to assign to each song, separated by spaces. type s to skip a song, type quit to exit.")
for song in songs:
    # Display Artist and Name of song. 
    track_str = song['name']
    track_str += " - "
    for artist in song['artists']:
        track_str += "{}, ".format(artist['name'])
    print(track_str)
    tags = input()
    tags = tags.strip()
    if 'quit' == tags:
        break
    elif 's' == tags:
        continue
    else:
        tags = tags.split()
        for tag in tags:
            insert_to_db(db_conn, song, sp.audio_features(song['id']), tag)

db_conn.close()