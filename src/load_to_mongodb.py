# Imports
import os
import pymongo
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv

# Setting Up the Connection & Connecting to the database

# Load environment variables
load_dotenv()

# Setting Up the Connection & Connecting to the database
CWL = os.getenv("CWL")
SNUM = os.getenv("SNUM")

if CWL is None or SNUM is None:
    print("CWL or SNUM not found in .env file.")
elif CWL.strip() == "" or SNUM.strip() == "":
    print("CWL or SNUM is empty in .env file.")
elif SNUM[0] == "a":
    print("You don't need to include the a here. Just include your student number as a string such as \"12345678\".")
else:
    connection_string = f"mongodb://{CWL}:a{SNUM}@localhost:27017/{CWL}"
    client = pymongo.MongoClient(connection_string)
    db = client[CWL]["movies_db"]
    movies_collection = db["movies"]

if __name__ == "__main__":
    # Transform Data for Document Structure
    # import cleaned data (from phase 3)
    basics_df = pd.read_csv("data/cleaned/basics_cleaned.csv")
    ratings_df = pd.read_csv("data/cleaned/ratings_cleaned.csv")
    trailers_df = pd.read_csv("data/cleaned/movie_sentiments_cleaned.csv")

    # remove duplicates temporarily (since movie_sentiments_cleaned still contains duplicates)
    # this should be removed in the later because our data should not contain duplicates
    trailers_df = trailers_df.drop_duplicates(subset=['name_norm'], keep='first')

    # merge basics and ratings on tconst
    movies_df = basics_df.merge(ratings_df, on='tconst', how='inner')

# remove duplicate movie titles to match schema design 
# duplicate movie titles in sentiment data are pulled from the same youtube video, hence only first occurrence kept
trailers_df = trailers_df.drop_duplicates(subset=['name_norm'], keep='first')

    # convert merged dataframe into list of nested dictionaries 
    # each row becomes a dictionary corresponding to a movie document
    movie_docs = movies_df_2.apply(
        lambda row: {
            "_id": row['tconst'],
            "primaryTitle_norm": row['primaryTitle_norm'],
            "primaryTitle": row['primaryTitle'],
            "startYear": int(row['startYear']),
            "ratings": {
                "averageRating": float(row['averageRating']),
                "numVotes": int(row['numVotes'])
            },
            "trailer": {
                "trailer_id": int(row['trailer_id']),
                "favorability": float(row['favorability']),
                "rating": row['rating'],
                "genre": row['genre'],
                "year": int(row['year'])
            }
        }, axis=1
    ).tolist()

    # Populating the Database

    # this is just in case you have an existing database with same name
    # we want to clear out that database before inserting data into it
    db.movies_collection.delete_many({})

    # insert list of movie documents into collection
    db.movies_collection.insert_many(movie_docs)

    # double check # of docs in collection (should match # of rows in merged dataset)
    print(db.movies_collection.count_documents({}))