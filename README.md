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

### Log
May 2024
1. Was using the explore notebook to get back into things and see the data

9th Oct 2024
1. Have a look to see if there are any clusters!!
1. Tried k-means on bones, did not really work as the results were pretty random by nature.  Try other types of cluster next time and other types of scores
1. tried dbscan and was also bad.  
1. maybe try to look into PCA to actually observe the clusters

15th Oct 2024
1. Need to normalise these variables!!! -> this made it worse somehow.  need to just do some studying of decent ways to do clustering because this is not working
1. just double checked that we could still separate the whole library into expected playlists - and we can.  therefore we either need better algorithm or more nuanced features
1. quick look on echo nest - features are exactly the same so need something better... I wonder if the spotify API has anything else we could leverage

4th June 2025
1. Lane switch - making my own data from my itunes collection. Used claude to generate a data generation script.  the resulting spectrograms will then be used in an autocoder to try and generate some patterns to be used later for clustering

20th June 2025
1. Need to look into the different channels because they are different sizes (heights).... maybe just look at spectrogram for now.

4th July 2025
1. Make a pipeline so we can save and look at the results of the images using the test set
1. Still getting my head around the way the autoencoder will actually WORK with convolutional stuff....

10th Oct 2025
1. Made a prediction pipeline to take a model, test dataset and which puts results into an appriopriately named results dir
1. Claire gave me some pointers as to where to explore next... tried increasing kernel size.  increased number of layers and step down to as small a CNN as possible before flattening. tried batch normalisation to try and keep the gradients alive.  but didn't properly work.  inspected gradients with `model.state_dict()` and could see the gradients vanishing.

NEXT: 
- need to look for remedies for the vanishing gradients.  maybe param optimiser tuning of hyp params.
- Simplify model a LOT (maybe remove flattening part) to just get some results which aren't ZERO 🤪.  Maybe an encoder could work in 2D???  
- should look into RNNs, TSNE 

### TODO
1. See if we have any hope in separating individual playlists by having a look at PCA
1. Update the playlist data with fresh songs
1. Test out a separation script of maybe just kmeans for suggesting splits - whichever one gives the best score - 1 - 5
1. Get main genres and sub genres for each of the songs in the splits and an associated album art.


