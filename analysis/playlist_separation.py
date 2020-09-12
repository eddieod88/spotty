import numpy as np
import pandas as pd
import sqlite3

from sklearn.mixture import BayesianGaussianMixture

"""
Script to determine subgroups of songs within a playlist that could potentially
be separated out into another playlist
"""


conn = sqlite3.connect('./data_collection/spotify-proj.db')

df = pd.read_sql_query("select * from beats_playlist;", conn)
df = df.drop(labels=['playlist'], axis=1)  # don't need the playlist label as assuming these tracks are all from beats.
types = {
    'acousticness': np.double,
    'danceability': np.double,
    'energy': np.double,
    'liveness': np.double,
    'loudness': np.double,
    'mode': np.double,
    'speechiness': np.double,
    'tempo': np.double,
    'valence': np.double,
    'instrumentalness': np.double,
}
df = df.astype(types)
X = df.drop(labels=['id ', 'artist', 'name', 'mode', 'tempo', 'loudness'], axis=1)

# Initial model to get appropriate number of clusters
bgmm = BayesianGaussianMixture(
    n_components=20,
    n_init=20,
)
bgmm.fit(X)
num_clusters = len([w for w in bgmm.weights_ if w > 0.05])

bgmm_2 = BayesianGaussianMixture(
    n_components=num_clusters,
    n_init=20
)

probs = pd.DataFrame(bgmm_2.fit(X).predict_proba(X))

results = pd.concat([df, probs], axis=1, sort=False)


# inital results - fluctuate a lot and also the weightings seem to do bugger all.

# TODO:
#  - REAAALLLY have a look at what features are actually important. instrumentallness is not one of them...
#  - DBSCAN is probs a pretty good way of getting the clusters actually - do a minimum value of like 10 songs
#  - then check out anomoly detection
#  - Look at the relative frequencies of all of the different features to see if there are
#    data issues. HAS TO be data issues
#  - See how many songs are above a certain threshold. Add songs to multiple playlists.
#  - If largest value is within 50% of the other one, and the max value is > 0.5, flag.
#    print(title_of_track, values)
#  - Graph of artists within and group.
#  - compare against a playlist with one genre...
