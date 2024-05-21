from collections import defaultdict
import yaml
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


class SpotifyFetch:
    def __init__(self, config_path: Path) -> None:
        # config contains features
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        load_dotenv()
        oauth = SpotifyOAuth(
            client_id=getenv("SPOTIPY_CLIENT_ID"),
            client_secret=getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-library-read",
        )
        self.sp = Spotify(auth_manager=oauth)

    def get_playlist_songs_for_user(self) -> pd.DataFrame:
        # get all playlist data for logged in user (tracks and audo features)
        # TODO: see the columns and compare against the config. log if there are new columns
        # filter the df to the config features
        # return df
        try:
            current_user = self.sp.me()
        except Exception as e:
            raise e
        user_id = current_user["id"]

        playlists = []
        offset = 0
        playlist_batch_num = 50
        while playlist_batch := self.sp.user_playlists(
            user_id, limit=playlist_batch_num, offset=offset
        )["items"]:
            playlists.extend(
                [p for p in playlist_batch if p["owner"].get("id") == user_id]
            )
            offset += playlist_batch_num

        selected_features = self.config["data"]["raw_features"]
        playlist_data = defaultdict(list)
        track_batch_num = 100
        for playlist in playlists:
            offset = 0
            # TODO: should use the fields kw to speed this up
            while tracks := (
                self.sp.playlist_items(
                    playlist["id"],
                    limit=track_batch_num,
                    offset=offset,
                    additional_types="track",
                ).get("items")
            ):
                offset += track_batch_num
                track_ids = []

                print(playlist["name"], len(tracks))
                for track in tracks:
                    t = track["track"]
                    if t["is_local"]:
                        # Won't have audio information - TODO: go straight to audio analyser
                        # TODO: should also collect this information in order to store the NaNs
                        continue
                    track_ids.append(t["id"])
                    playlist_data["playlist_name"].append(playlist["name"])
                    playlist_data["artist"].append(t["artists"][0]["name"])
                    if len(t["artists"]) > 1:
                        playlist_data["artist_features"].append(
                            "|".join(
                                [f_artist["name"] for f_artist in t["artists"][1:]]
                            )
                        )
                    else:
                        playlist_data["artist_features"].append(None)
                    playlist_data["name"].append(t["name"])
                    playlist_data["album"].append(t["album"]["name"])
                playlist_data["id"].extend(track_ids)
                if track_ids:
                    audio_features = self.sp.audio_features(track_ids)
                    for feature in selected_features:
                        playlist_data[feature].extend(
                            [af[feature] for af in audio_features]
                        )
        return pd.DataFrame(playlist_data)
