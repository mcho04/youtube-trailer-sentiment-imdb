-- .headers on
-- .mode column

-- SELECT * FROM movies
-- LIMIT 5;

-- SELECT * FROM ratings
-- LIMIT 5;

-- SELECT * FROM movie_sentiments
-- LIMIT 5;

-- SELECT ms.genre, ms.favorability, r.averageRating
-- FROM movies m 
-- JOIN ratings r ON m.tconst = r.tconst
-- JOIN movie_sentiments ms ON m.primaryTitle_norm = ms.name_norm
-- WHERE ms.genre IN ('Action', 'Comedy');

-- SELECT 
--     CASE 
--         WHEN r.averageRating >= 7 THEN 'High'
--         WHEN r.averageRating <= 4 THEN 'Low'
--     END AS rating_group,
--     ms.favorability,
--     r.averageRating
-- FROM basics b
-- JOIN ratings r ON b.tconst = r.tconst
-- JOIN movie_sentiments ms ON b.primaryTitle_norm = ms.name_norm
-- WHERE r.averageRating >= 7 OR r.averageRating <= 4
-- ORDER BY rating_group

-- SELECT 
--     ms.rating,
--     CASE 
--         WHEN ms.rating = 'R' THEN 'R-Rated'
--         ELSE 'Non R-Rated'
--     END AS rating_group,
--     r.averageRating,
--     ms.favorability
-- FROM basics b
-- JOIN ratings r ON b.tconst = r.tconst
-- JOIN movie_sentiments ms ON b.primaryTitle_norm = ms.name_norm
-- WHERE ms.rating IN ('R', 'PG', 'PG-13', 'G')
-- ORDER BY rating_group, r.averageRating