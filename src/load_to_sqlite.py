import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("data/database/movies.db")
BASICS_CSV = Path("data/cleaned/basics_cleaned.csv")
RATINGS_CSV = Path("data/cleaned/ratings_cleaned.csv")
SENTIMENTS_CSV = Path("data/cleaned/movie_sentiments_cleaned.csv")

def create_tables(cursor):
    cursor.execute("DROP TABLE IF EXISTS movie_sentiments")
    cursor.execute("DROP TABLE IF EXISTS ratings")
    cursor.execute("DROP TABLE IF EXISTS movies")
    cursor.execute("""
    CREATE TABLE movies (
        tconst TEXT PRIMARY KEY,
        primaryTitle_norm TEXT,
        primaryTitle TEXT,
        startYear INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE ratings (
        tconst TEXT,
        averageRating REAL,
        numVotes INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE movie_sentiments (
        trailer_id TEXT PRIMARY KEY,
        name_norm TEXT,
        favorability REAL,
        rating TEXT,
        genre TEXT,
        year INTEGER
    )
    """)

def load_movies(cursor, df):
    rows = list(df[["tconst", "primaryTitle_norm", "primaryTitle", "startYear"]].itertuples(index=False, name=None))
    cursor.executemany(
        """
        INSERT INTO movies (tconst, primaryTitle_norm, primaryTitle, startYear)
        VALUES (?, ?, ?, ?)
        """,
        rows,
    )

def load_ratings(cursor, df):
    rows = list(df[["tconst", "averageRating", "numVotes"]].itertuples(index=False, name=None))
    cursor.executemany(
        """
        INSERT INTO ratings (tconst, averageRating, numVotes)
        VALUES (?, ?, ?)
        """,
        rows,
    )

def load_sentiments(cursor, df):
    deduped_df = df.drop_duplicates(subset=["trailer_id"]).copy()
    dropped_rows = len(df) - len(deduped_df)
    if dropped_rows:
        print(f"Dropped {dropped_rows} duplicate movie_sentiments rows by trailer_id.")
    rows = list(
        deduped_df[
            ["trailer_id", "name_norm", "favorability", "rating", "genre", "year"]
        ].itertuples(index=False, name=None)
    )
    cursor.executemany(
        """
        INSERT INTO movie_sentiments (trailer_id, name_norm, favorability, rating, genre, year)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

def main():
    basics_df = pd.read_csv(BASICS_CSV)
    ratings_df = pd.read_csv(RATINGS_CSV)
    sentiments_df = pd.read_csv(SENTIMENTS_CSV)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        create_tables(cursor)
        load_movies(cursor, basics_df)
        load_ratings(cursor, ratings_df)
        load_sentiments(cursor, sentiments_df)
        conn.commit()
        print("Loaded cleaned data into data/database/movies.db")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()