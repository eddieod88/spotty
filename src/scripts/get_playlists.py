from pathlib import Path

from src.data.fetch import SpotifyFetch

ROOT = Path(__file__).parents[2]

playlist_path = ROOT / "data/raw_data/user_playlists.csv"
config_path = ROOT / "config.yaml"

SpotifyFetch(config_path).get_playlist_songs_for_user().to_csv(playlist_path)
