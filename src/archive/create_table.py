import sqlite3


def main():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        tconst TEXT PRIMARY KEY,
        primaryTitle_norm TEXT,
        startYear INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        tconst TEXT,
        averageRating REAL,
        numVotes INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movie_sentiments (
        name_norm TEXT,
        trailer_link TEXT,
        video_id TEXT PRIMARY KEY,
        positive REAL,
        neutral REAL,
        negative REAL,
        favorability REAL,
        rating REAL,
        genre TEXT,
        year INTEGER,
        votes INTEGER
    )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully")


if __name__ == "__main__":
    main()