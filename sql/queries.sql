.headers on
.mode column

SELECT COUNT(*) AS movie_count FROM movies;

SELECT COUNT(*) AS ratings_count FROM ratings;

SELECT COUNT(*) AS sentiment_count FROM movie_sentiments;

SELECT *
FROM movies
LIMIT 10;

SELECT *
FROM ratings
LIMIT 10;

SELECT *
FROM movie_sentiments
LIMIT 10;

SELECT m.primaryTitle, m.startYear, r.averageRating, r.numVotes
FROM movies AS m
JOIN ratings AS r
    ON m.tconst = r.tconst
LIMIT 10;

SELECT genre, AVG(favorability) AS avg_favorability
FROM movie_sentiments
GROUP BY genre
ORDER BY avg_favorability DESC;
