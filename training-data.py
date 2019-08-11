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
"""

import sqlite3

def get_db_conn(path) -> sqlite3.Connection:
    pass

def select_playlist():
    """
        - Return a list of Songs in any order. 
        - Only include songs which are not in the db. 
    """
    pass

def check_tag_exists(tag):
    pass

def enter_to_db(db, song, tag):
    pass