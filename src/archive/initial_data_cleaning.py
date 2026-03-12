import numpy as np
import pandas as pd
import re

basics_path = 'data/raw/title.basics.tsv'
ratings_path = 'data/raw/title.ratings.tsv'
movie_sentiments_path = 'data/raw/movies_youtube_sentiments.csv'

## FUNCTIONS

# normalizes movie titles (convert to lowercase, remove punctuation, trim extra whitespaces)
# assume all null titles were removed, hence skip this edge case
def normalize_title(title):
    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)   
    title = re.sub(r"\s+", " ", title)      
    return title.strip()


## DATA LOADING & CLEANING
basics = pd.read_csv(basics_path, sep='\t', na_values="\\N", low_memory=False)
ratings = pd.read_csv(ratings_path, sep='\t')
movie_sentiments = pd.read_csv(movie_sentiments_path)

print("Size of basics data", basics.shape) # (12246013, 9)
print("Size of ratings data", ratings.shape) # (1629185, 3)
print("Size of movie sentiments data", movie_sentiments.shape) #(1105, 18)

# check data types of variables
print("Data types of Basics datasets:", basics.dtypes)
print("Data types of ratings datasets:", ratings.dtypes)


# BASICS DATASET

# keep only movie titles in basics
basics = basics[basics['titleType'] == 'movie']
print("Size of basics data with only movies", basics.shape) # (738446, 9)

# convert startYear and endYear to integer
basics['startYear'] = basics['startYear'].astype('Int64')
basics['endYear'] = basics['endYear'].astype('Int64')

# keep only movies released between 2005 and 2019
basics = basics[(basics['startYear'] >= 2005) & (basics['startYear'] <= 2019)]
print("Size of basics data with only movies from 2005-2019", basics.shape) # (217972, 9)

# check whether primaryTitle has null titles, if true then remove that row
basics.info()
basics = basics.dropna(subset=['primaryTitle'])
print("Size of basics data with only movies from 2005-2019 and non null titles", basics.shape) # (217970, 9)

# normalize primaryTitle 
basics['primaryTitle_norm'] = basics['primaryTitle'].apply(normalize_title)

# keep variables of interest
basics = basics[
    ["tconst",
     "primaryTitle_norm",
     "primaryTitle",
     "startYear"]
]


# RATINGS DATASET

# keep variables of interest
ratings = ratings[
    ["tconst",
     "averageRating",
     "numVotes"]
]


# MOVIE SENTIMENTS DATASET

# check whether primaryTitle has null titles, if true then remove that row
movie_sentiments.info()
movie_sentiments = movie_sentiments.dropna(subset=['rating'])
print("Size of movie sentiments data with only movies with a rating", movie_sentiments.shape) # (1104, 18)

# normalize titles in kaggle dataset
movie_sentiments['name_norm'] = movie_sentiments['name'].apply(normalize_title)

# keep variables of interest
movie_sentiments = movie_sentiments[
        [
        "name_norm",
        "trailer_link",
        "video_id",
        "sentiment_scores",
        "favorability",
        "rating",
        "genre",
        "year",
        "votes"
    ]
]

## EXPORT CLEANED DATASET
basics.to_csv("data/cleaned/basics_cleaned.csv", index=False)

# Export IMDb ratings
ratings.to_csv("data/cleaned/ratings_cleaned.csv", index=False)

# Export Kaggle YouTube movie data
movie_sentiments.to_csv("data/cleaned/movie_sentiments_cleaned.csv", index=False)