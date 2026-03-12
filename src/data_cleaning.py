import numpy as np
import pandas as pd
import re

basics_path = 'youtube-trailer-sentiment-imdb/data/raw/title.basics.tsv'
ratings_path = 'youtube-trailer-sentiment-imdb/data/raw/title.ratings.tsv'
movie_sentiments_path = 'youtube-trailer-sentiment-imdb/data/raw/movies_youtube_sentiments.csv'

## FUNCTIONS

# normalizes movie titles (convert to lowercase, remove punctuation, trim extra whitespaces)
# assume all null titles were removed, hence skip this edge case
def normalize_title(title):
    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)   
    title = re.sub(r"\s+", " ", title)      
    return title.strip()


## DATA LOADING 
def load_data():
    basics = pd.read_csv(basics_path, sep='\t', na_values="\\N", low_memory=False)
    ratings = pd.read_csv(ratings_path, sep='\t')
    movie_sentiments = pd.read_csv(movie_sentiments_path)
    return basics, ratings, movie_sentiments

# print("Size of basics data", basics.shape) # (12246013, 9)
# print("Size of ratings data", ratings.shape) # (1629185, 3)
# print("Size of movie sentiments data", movie_sentiments.shape) #(1105, 18)

# check data types of variables
# print("Data types of Basics datasets:", basics.dtypes)
# print("Data types of ratings datasets:", ratings.dtypes)


## DATA CLEANING

# BASICS DATASET
def clean_basics(basics): # initial size: (12246013, 9)
    basics = basics[basics['titleType'] == 'movie'].copy() # keep only movie titles in basics # size: (738446, 9)
    basics['startYear'] = basics['startYear'].astype('Int64') # convert startYear and endYear to integer
    basics['endYear'] = basics['endYear'].astype('Int64') # convert startYear and endYear to integer
    basics = basics[(basics['startYear'] >= 2005) & (basics['startYear'] <= 2019)].copy() # keep only movies released between 2005 and 2019 # size: (217972, 9)
    basics = basics.dropna(subset=['primaryTitle']).copy() # ran basics.info() to check for nulls, and remove them # size: (217970, 9)
    basics['primaryTitle_norm'] = basics['primaryTitle'].apply(normalize_title)

    return basics[["tconst","primaryTitle_norm","primaryTitle","startYear"]]


# RATINGS DATASET

def clean_ratings(ratings):
    return ratings[["tconst","averageRating","numVotes"]] # keep variables of interest # (1629185, 3)

# MOVIE SENTIMENTS DATASET

def clean_sentiments(movie_sentiments): # initial size: (1105, 18)
    movie_sentiments = movie_sentiments.dropna(subset=['rating']).copy() # (1104, 18)
    movie_sentiments['name_norm'] = movie_sentiments['name'].apply(normalize_title)

    return movie_sentiments[
        ["name_norm","trailer_link","video_id","sentiment_scores",
         "favorability","rating","genre","year","votes"]
    ]

def export_cleaned_data(basics, ratings, movie_sentiments):
    basics.to_csv("data/cleaned/basics_cleaned.csv", index=False)
    ratings.to_csv("data/cleaned/ratings_cleaned.csv", index=False)
    movie_sentiments.to_csv("data/cleaned/movie_sentiments_cleaned.csv", index=False)


def main():
    basics, ratings, movie_sentiments = load_data()
    print("Data loaded")

    basics = clean_basics(basics)
    print("Basics cleaned:", basics.shape)

    ratings = clean_ratings(ratings)
    print("Ratings cleaned:", ratings.shape)

    movie_sentiments = clean_sentiments(movie_sentiments)
    print("Sentiments cleaned:", movie_sentiments.shape)

    export_cleaned_data(basics, ratings, movie_sentiments)
    print("Cleaned files exported")    


if __name__ == "__main__":
    main()
