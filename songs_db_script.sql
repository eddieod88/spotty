CREATE TABLE Song (
    _id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    Title               VARCHAR(255),
    Artist              VARCHAR(255),
    Album               VARCHAR(255),
    Acousticness        REAL,
    Danceability        REAL,
    Energy              REAL,
    Instrumentalness    REAL,
    MusicalKey          REAL,
    Liveness            REAL,
    Speechiness         REAL,
    Tempo               REAL,
    Valence             REAL,
    Tag               VARCHAR(255),
    FOREIGN KEY (Tag) REFERENCES Tag(Name)
);

CREATE TABLE Tag (
    _id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    Name                VARCHAR(255) UNIQUE
);