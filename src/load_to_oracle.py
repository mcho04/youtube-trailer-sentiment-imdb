from pathlib import Path
import pandas as pd
import oracledb
import os
from dotenv import load_dotenv

# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================
from dotenv import load_dotenv
load_dotenv()

# =========================
# FILE PATHS
# =========================
BASICS_CSV = Path("data/cleaned/basics_cleaned.csv")
RATINGS_CSV = Path("data/cleaned/ratings_cleaned.csv")
SENTIMENTS_CSV = Path("data/cleaned/movie_sentiments_cleaned.csv")

# =========================
# ORACLE CONNECTION INFO
# Type your own credentials in terminal
# Example: 
# export ORACLE_USER = YOUR_USERNAME
# export ORACLE_PASSWORD = YOUR PASSWORD
# =========================
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = "localhost:1522/stu"

# =========================
# HELPER FUNCTIONS
# =========================
def drop_table(cursor, table_name):
    """
    Drop a table if it exists.
    Ignores ORA-00942: table or view does not exist.
    """
    try:
        cursor.execute(f"DROP TABLE {table_name} CASCADE CONSTRAINTS")
        print(f"Dropped table {table_name}")
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        if error_obj.code == 942:
            print(f"Table {table_name} does not exist, skipping drop")
        else:
            raise

def create_tables(cursor):
    drop_table(cursor, "MOVIE_SENTIMENTS")
    drop_table(cursor, "RATINGS")
    drop_table(cursor, "MOVIES")

    cursor.execute("""
        CREATE TABLE MOVIES (
            TCONST            VARCHAR2(20) PRIMARY KEY,
            PRIMARYTITLE_NORM VARCHAR2(500),
            PRIMARYTITLE      VARCHAR2(500),
            STARTYEAR         NUMBER(4)
        )
    """)

    cursor.execute("""
        CREATE TABLE RATINGS (
            TCONST         VARCHAR2(20),
            AVERAGERATING  NUMBER(3,1),
            NUMVOTES       NUMBER,
            CONSTRAINT FK_RATINGS_MOVIES
                FOREIGN KEY (TCONST) REFERENCES MOVIES(TCONST)
        )
    """)

    cursor.execute("""
        CREATE TABLE MOVIE_SENTIMENTS (
            TRAILER_ID    VARCHAR2(100) PRIMARY KEY,
            NAME_NORM     VARCHAR2(500),
            FAVORABILITY  NUMBER(10,6),
            RATING        VARCHAR2(50),
            GENRE         VARCHAR2(100),
            YEAR          NUMBER(4)
        )
    """)

    print("Tables created successfully")

def clean_null(value):
    """
    Convert pandas NaN to Python None for Oracle inserts.
    """
    if pd.isna(value):
        return None
    return value

# =========================
# LOAD FUNCTIONS
# =========================

def load_movies(cursor, df):
    rows = [
        (
            clean_null(row["tconst"]),
            clean_null(row["primaryTitle_norm"]),
            clean_null(row["primaryTitle"]),
            clean_null(row["startYear"]),
        )
        for _, row in df.iterrows()
    ]

    # executemany is used for efficiency when inserting many rows.
    cursor.executemany("""
        INSERT INTO MOVIES (TCONST, PRIMARYTITLE_NORM, PRIMARYTITLE, STARTYEAR)
        VALUES (:1, :2, :3, :4)
    """, rows)

    print(f"Inserted {len(rows)} rows into MOVIES")

def load_ratings(cursor, df):
    rows = [
        (
            clean_null(row["tconst"]),
            clean_null(row["averageRating"]),
            clean_null(row["numVotes"]),
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany("""
        INSERT INTO RATINGS (TCONST, AVERAGERATING, NUMVOTES)
        VALUES (:1, :2, :3)
    """, rows)

    print(f"Inserted {len(rows)} rows into RATINGS")

def load_sentiments(cursor, df):
    deduped_df = df.drop_duplicates(subset=["trailer_id"]).copy()
    dropped_rows = len(df) - len(deduped_df)

    if dropped_rows:
        print(f"Dropped {dropped_rows} duplicate MOVIE_SENTIMENTS rows by trailer_id")

    rows = [
        (
            clean_null(row["trailer_id"]),
            clean_null(row["name_norm"]),
            clean_null(row["favorability"]),
            clean_null(row["rating"]),
            clean_null(row["genre"]),
            clean_null(row["year"]),
        )
        for _, row in deduped_df.iterrows()
    ]

    cursor.executemany("""
        INSERT INTO MOVIE_SENTIMENTS
        (TRAILER_ID, NAME_NORM, FAVORABILITY, RATING, GENRE, YEAR)
        VALUES (:1, :2, :3, :4, :5, :6)
    """, rows)

    print(f"Inserted {len(rows)} rows into MOVIE_SENTIMENTS")


# =========================
# RUN THE FULL ORACLE LOADING PIPELINE
# =========================
def main():
    basics_df = pd.read_csv(BASICS_CSV)
    ratings_df = pd.read_csv(RATINGS_CSV)
    sentiments_df = pd.read_csv(SENTIMENTS_CSV)

    if not ORACLE_USER or not ORACLE_PASSWORD or not ORACLE_DSN:
        raise ValueError("Missing ORACLE_USER, ORACLE_PASSWORD, or ORACLE_DSN environment variable.")

    conn = oracledb.connect(
        user=ORACLE_USER,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN,
    )

    cursor = conn.cursor()

    try:
        create_tables(cursor)
        load_movies(cursor, basics_df)
        load_ratings(cursor, ratings_df)
        load_sentiments(cursor, sentiments_df)

        conn.commit()
        print("Loaded cleaned CSV data into Oracle successfully")

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()