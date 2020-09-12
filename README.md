# Spotify Projects

This repo contains a mixed bag of scripts related to a few spotify ML projects/ideas that I have been working on 

## Project 1 - Tag Prediction

_Given a set of songs in a library which have been assigned one or many tags describing the mood of each song, predict the tags which should be applied to new songs in which a user wants to add to their library._

Spotify's Echonest data set of song characteristics have been used to provide the features of this problem. 


### Stage 1 - Binary Classification

Classify whether a song belongs to one tag or another. Logistic regression used.

### Stage 2 - Multi-Class Classification

Classify which tag a song should be assigned with based on a number of options. Multi-value Logistic regression used or SVM   

### Stage 3 - Multi-Class Multi-Value Classification

Determine which collection of tags a song should be assigned, given a choice of multiple tags. TBC...


## Project 2 - Playlist separator

This project tries to address the issue in which someone's music playlists evolve over time and eventually become a mess
 regardless how neat they started
 
Used clustering algorithms to try and find groups within playlists which could suggest to a user a split in a playlist 