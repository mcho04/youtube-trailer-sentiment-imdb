import os
import pandas as pd
import oracledb

BASICS_CSV = "data/cleaned/basics_cleaned.csv"
RATINGS_CSV = "data/cleaned/ratings_cleaned.csv"
SENTIMENTS_CSV = "data/cleaned/movie_sentiments_cleaned.csv"

# Connect to Oracle database
def get_connection():
    return oracledb.connect(
        user=os.getenv("UBC_ORACLE_USER"),
        password=os.getenv("UBC_ORACLE_PASSWORD"),
        dsn=os.getenv("UBC_ORACLE_DSN")
    )

# NOTE: Make sure to set up the environment variables before running the script.
# To set up the environment variables, run the following commands:
# export UBC_ORACLE_USER="your_username"
# export UBC_ORACLE_PASSWORD="your_password"
# export UBC_ORACLE_DSN="your_dsn"


# Drop tables if they exist
def drop_tables(cursor):
    tables = ["movie_sentiments", "ratings", "basics"]

    for table in tables:
        try:
            cursor.execute(f"DROP TABLE {table} PURGE")
            print(f"Dropped table: {table}")
        except oracledb.DatabaseError:
            print(f"Table {table} does not exist, skipping drop.")

# Create basics table
def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE basics (
            tconst VARCHAR2(20) PRIMARY KEY,
            primaryTitle_norm VARCHAR2(300),
            primaryTitle VARCHAR2(300),
            startYear NUMBER
        )
    """)
# Create ratings table
    cursor.execute("""
        CREATE TABLE ratings (
            tconst VARCHAR2(20),
            averageRating NUMBER,
            numVotes NUMBER
        )
    """)

# Create movie_sentiments table
    cursor.execute("""
        CREATE TABLE movie_sentiments (
            name_norm VARCHAR2(300),
            trailer_link VARCHAR2(500),
            video_id VARCHAR2(50) PRIMARY KEY,
            sentiment_scores VARCHAR2(1000),
            favorability NUMBER,
            rating VARCHAR2(20),
            genre VARCHAR2(100),
            year NUMBER,
            votes NUMBER
        )
    """)

    print("Tables created.")

# Load basics table into Oracle database
def load_basics(cursor, basics_df):
    rows = list(basics_df.itertuples(index=False, name=None))
    cursor.executemany("""
        INSERT INTO basics (tconst, primaryTitle_norm, primaryTitle, startYear)
        VALUES (:1, :2, :3, :4)
    """, rows)

    print(f"Inserted {len(rows)} rows into basics.")

# Load ratings table into Oracle database
def load_ratings(cursor, ratings_df):
    rows = list(ratings_df.itertuples(index=False, name=None))

    cursor.executemany("""
        INSERT INTO ratings (tconst, averageRating, numVotes)
        VALUES (:1, :2, :3)
    """, rows)

    print(f"Inserted {len(rows)} rows into ratings.")

# Load movie_sentiments table into Oracle database
def load_sentiments(cursor, sentiments_df):
    rows = list(sentiments_df.itertuples(index=False, name=None))

    cursor.executemany("""
        INSERT INTO movie_sentiments (
            name_norm, trailer_link, video_id, sentiment_scores,
            favorability, rating, genre, year, votes
        )
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
    """, rows)

    print(f"Inserted {len(rows)} rows into movie_sentiments.")

# Main function
def main():
    basics_df = pd.read_csv(BASICS_CSV)
    ratings_df = pd.read_csv(RATINGS_CSV)
    sentiments_df = pd.read_csv(SENTIMENTS_CSV)

    print("Cleaned CSV files loaded.")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        drop_tables(cursor)
        create_tables(cursor)

        load_basics(cursor, basics_df)
        load_ratings(cursor, ratings_df)
        load_sentiments(cursor, sentiments_df)

        connection.commit()
        print("Commit successful.")

    except Exception as e:
        connection.rollback()
        print("Error occurred. Rolled back transaction.")
        print(e)

    finally:
        cursor.close()
        connection.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()