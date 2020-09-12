import numpy as np
import pandas as pd
import sqlite3

from sklearn.mixture import BayesianGaussianMixture
from sklearn.model_selection import train_test_split

conn = sqlite3.connect('../data_collection/binary.db')

query = (
    "select s._id, s.Title, s.Artist, s.Album, s.Acousticness, s.Danceability, s.Energy, s.Instrumentalness, "
    "s.MusicalKey, s.Liveness, s.Tempo, s.Valence, t.Name as Tag from Relationship as r\n"
    "join Song as s on s._id = r.Song_id\n"
    "join Tag as t on t._id = r.Tag_id;"
)

df = pd.read_sql_query(query, conn)

X = df.drop(labels=['_id', 'Title', 'Artist', 'Album', 'MusicalKey', 'Tempo', 'Tag'], axis=1)
y = df['Tag']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
k_value = 2
bgmm = BayesianGaussianMixture(n_components=k_value)
bgmm.fit(X_train)

probs = bgmm.predict_proba(X_test)
