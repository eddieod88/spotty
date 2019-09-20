DROP TABLE IF EXISTS Relationship;
DROP TABLE IF EXISTS Tag;
DROP TABLE IF EXISTS Song;

CREATE TABLE Song (
    _id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    Title                   VARCHAR(255),
    Artist                  VARCHAR(255),
    Album                   VARCHAR(255),
    Acousticness            REAL,
    Danceability            REAL,
    Energy                  REAL,
    Instrumentalness        REAL,
    MusicalKey              REAL,
    Liveness                REAL,
    Speechiness             REAL,
    Tempo                   REAL,
    Valence                 REAL,
    UNIQUE (Title, Artist, Album)
);

CREATE TABLE Tag (
    _id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    Name                    VARCHAR(255) UNIQUE
);

CREATE TABLE Relationship (
    _id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    Song_id                 INTEGER,
    Tag_id                  VARCHAR(255),
    FOREIGN KEY (Song_id)   REFERENCES Song(_id),
    FOREIGN KEY (Tag_id)       REFERENCES Tag(_id)
);

-- Useful commands:
-- 1. standard data set (without tempo as it is not normalised)
--  select Song._id, Acousticness, Danceability, Energy, Instrumentalness, MusicalKey, Liveness, Speechiness, Valence, Relationship.Tag_id from Song JOIN Relationship ON Song._id=Relationship.Song_id;
