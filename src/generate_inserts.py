import numpy as np
import pandas as pd
import re

import pandas as pd

basics = pd.read_csv("data/cleaned/basics_cleaned.csv")
ratings = pd.read_csv("data/cleaned/ratings_cleaned.csv")
movie_sentiments = pd.read_csv("data/cleaned/movie_sentiments_cleaned.csv")


def generate_inserts(df, table_name, columns, output_file):
    with open(output_file, "a") as f:  # append mode
        for _, row in df.iterrows():

            # skip rows with missing values
            if any(pd.isna(row[col]) for col in columns):
                continue

            values = []
            for col in columns:
                val = row[col]

                if isinstance(val, str):
                    val = val.replace("'", "''")  # escape quotes
                    values.append(f"'{val}'")
                else:
                    values.append(str(val))
 
            values_str = ", ".join(values)
            cols_str = ", ".join(columns)

            insert_stmt = f"INSERT INTO {table_name} ({cols_str}) VALUES ({values_str});\n"

            f.write(insert_stmt)

generate_inserts(
    basics,
    "movies",
    ["tconst", "primaryTitle_norm", "startYear"],
    "sql/insert_data.sql"
)

generate_inserts(
    ratings,
    "ratings",
    ["tconst", "averageRating", "numVotes"],
    "sql/insert_data.sql"
)

generate_inserts(
    movie_sentiments,
    "movie_sentiments",
    ["name_norm", "trailer_link", "video_id", "positive", "neutral", "negative",
    "favorability", "rating", "genre", "year", "votes"],
    "sql/insert_data.sql"
)