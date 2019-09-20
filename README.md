# Spotify Tag Predictor

This is an ongoing Python supervised machine learning project which aims to solve the following typical classification problem:

_Given a set of songs in a library which have been assigned one or many tags describing the mood of each song, predict the tags which should be applied to new songs in which a user wants to add to their library._

Spotify's Echonest data set of song characteristics have been used to provide the features of this problem. SciPy algorithms have been used to create the model.


##Stories
### Stage 1 - Binary Classification

Classify whether a song belongs to one tag or another. Logistic regression used.

### Stage 2 - Multi-Class Classification

Classify which tag a song should be assigned with based on a number of options. Multi-value Logistic regression used or SVM   

### Stage 3 - Multi-Class Multi-Value Classification

Determine which collection of tags a song should be assigned, given a choice of multiple tags. TBC...

## Installation

Conda is used for this project. Download conda, then use the following command it initiate the required conda environment:

```
conda create -n tags -f requirements.yml
```

You can then use the command, ```conda activate tags``` to enter your conda python env.

## Current Status

Binary classification is working ok.

## Usage

Currently in developing stage so there is no program to run as such. Tests are being used to ensure that each function works as it should. The 'algorithm_test_data.csv' and 'binary_dnb_ambient.csv' are being used in the test_classification.py file at the moment.


## Tests

There are a number of unit tests which verify the workings of each step in the process. These are in the 'tests' directory 