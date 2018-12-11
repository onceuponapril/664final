-- Data set: https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings (22 Dec 2016)

--
-- 1.0 Setup. Delete tables after every build iteration.
--
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS movie, director, actor, genre, ,
                     , rating;
SET FOREIGN_KEY_CHECKS=1;

--
-- 2.0 ENTITIES
-- Serve as lookup tables
--

--
-- 2.1 genre table
--
CREATE TABLE IF NOT EXISTS genre (
  genre_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  genre_name VARCHAR(25) NOT NULL UNIQUE,
  PRIMARY KEY (genre_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movies/zfp-genres_unique.csv'
INTO TABLE genre
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  (genre_name);

--
-- 2.2 director table
--
CREATE TABLE IF NOT EXISTS director (
  director_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  director_name VARCHAR(10) NOT NULL UNIQUE,
  director_facebook_likes INTEGER NOT NULL,
  PRIMARY KEY (director_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movies/zfp-directors.csv'
INTO TABLE director
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  (director_name,director_facebook_likes);

--
-- 2.3 keyword table
--
CREATE TABLE IF NOT EXISTS keyword (
  keyword_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  keyword VARCHAR(100) NOT NULL UNIQUE,
  PRIMARY KEY (keyword_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movies/zfp-keywords_unique.csv'
INTO TABLE publisher
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  (keyword);

-- How about Language,Score ?
-- -- 2.4 rating table
-- --
-- CREATE TABLE IF NOT EXISTS rating (
--   rating_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
--   rating_name CHAR(4) NOT NULL UNIQUE,
--   PRIMARY KEY (rating_id)
-- )
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

-- LOAD DATA LOCAL INFILE './output/movies/zfp_ratings.csv'
-- INTO TABLE rating
--   CHARACTER SET utf8mb4
--   FIELDS TERMINATED BY '\t'
--   ENCLOSED BY '"'
--   LINES TERMINATED BY '\n'
--   (rating_name);

--
-- -- 2.5 country table
-- --
-- CREATE TABLE IF NOT EXISTS country (
--   country_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
--   country_name VARCHAR(25) NOT NULL UNIQUE,
--   PRIMARY KEY (country_id)
-- )
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

-- INSERT IGNORE INTO country (country_name) VALUES
--   ('Global'), ('North America'), ('Europe'), ('Japan'), ('Other');
-- 
--
-- 3.0 CORE ENTITIES AND M2M TABLES (developer, game, game_developer, sale)
--

--
-- 3.1 Temporary movie table
-- Note:  rows data set.
--
CREATE TEMPORARY TABLE temp_movie (
  movie_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  movie_title VARCHAR(255) NOT NULL,
  title_year INTEGER NULL,
  language_name VARCHAR(50),
  country VARCHAR(25) NULL,
  rating_name CHAR(6) NULL,
  imdb_score CHAR(3) NULL,
  duration CHAR(3) NULL,
  director_name VARCHAR(100) NULL,
  actor_name VARCHAR(100) NULL,
--   actor_1_name VARCHAR(100) NULL,
--   actor_2_name VARCHAR(100) NULL,
--   actor_3_name VARCHAR(100) NULL,
  genre VARCHAR(10) NULL,
  plot_keywords VARCHAR(100) NULL,
  PRIMARY KEY (movie_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movies/zfp-movie_metadata-trimmed.csv'
INTO TABLE temp_game
  CHARACTER SET utf8mb4
  -- FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  country VARCHAR(25) NULL,
  (movie_title, title_year, language_name, country,rating_name,
  imdb_score, duration, director_name, actor_1_name, actor_2_name,
  actor_3_name, genre, plot_keywords)

  SET movie_title = IF(movie_title = '', NULL, TRIM(movie_title)),
  title_year = IF(year_released = '', NULL, title_year),
  language_name = IF(language_name = '', NULL, language_name),
  publisher_name = IF(publisher_name = '', NULL, TRIM(publisher_name)),
  country = IF(country = '', NULL, country),
  rating_name = IF(rating_name = '', NULL, rating_name),
  imdb_score = IF(imdb_score = '', NULL, imdb_score),
  duration = IF(duration = '', NULL, duration),
  director_name = IF(director_name = '', NULL, TRIM(director_name)),
--   actor_1_name = IF(actor_1_name = '', NULL, TRIM(actor_1_name));
--   actor_2_name = IF(actor_1_name = '', NULL, TRIM(actor_1_name));
--   actor_3_name = IF(actor_1_name = '', NULL, TRIM(actor_1_name));
  genre = IF(genre = '', NULL, TRIM(genre));
  plot_keywords = IF(plot_keywords = '', NULL, TRIM(plot_keywords));

--
-- 3.2 movie table
-- Note: 5000+ rows data set 
-- Several columns will be dropped after junction tables are populated.
--
CREATE TABLE IF NOT EXISTS movie (
    movie_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    movie_title VARCHAR(255) NULL,
    title_year INTEGER NULL,
    language_name VARCHAR(50),
    country VARCHAR(25) NULL,
    rating_name CHAR(6) NULL,
    imdb_score CHAR(3) NULL,
    duration CHAR(3) NULL,
    director_id INTEGER NULL,
    -- actor_id INTEGER NULL,
    -- keyword_id INTEGER NULL,
    PRIMARY KEY (movie_id),
    FOREIGN KEY (director_id) REFERENCES director(director_id)
    ON DELETE CASCADE ON UPDATE CASCADE
    -- FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
    -- ON DELETE CASCADE ON UPDATE CASCADE,
    -- FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)
    -- ON DELETE CASCADE ON UPDATE CASCADE,
    -- FOREIGN KEY (rating_id) REFERENCES rating(rating_id)
    -- ON DELETE CASCADE ON UPDATE CASCADE
  )
  ENGINE=InnoDB
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO movie
(
    movie_id,
    movie_title,
    title_year,
    language_name,
    country,
    rating_name,
    imdb_score,
    duration,
    director_id,
)
SELECT tm.movie_title, director.director_id
    --     CAST(tg.year_released AS UNSIGNED) AS year_released,
    --    g.genre_id, pub.publisher_id,
    --    tg.north_america_sales, tg.europe_sales, tg.japan_sales, tg.other_sales, tg.global_sales,
    --    CAST(tg.critic_score AS UNSIGNED) AS critic_score,
    --    CAST(tg.critic_count AS UNSIGNED) AS critic_count,
    --    CAST(tg.user_score AS UNSIGNED) AS user_score,
    --    CAST(tg.user_count AS UNSIGNED) AS user_count,
    --    tg.developer_name, r.rating_id
 FROM temp_movie tm
      LEFT JOIN director d
             ON TRIM(tm.director_id) = TRIM(d.director)
    --   LEFT JOIN platform plat
    --          ON TRIM(tg.platform_name) = TRIM(plat.platform_name)
    --   LEFT JOIN publisher pub
    --          ON TRIM(tg.publisher_name) = TRIM(pub.publisher_name)
    --   LEFT JOIN rating r
    --          ON TRIM(tg.rating_name) = TRIM(r.rating_name)
WHERE tm.movie_title IS NOT NULL AND tm.movie_title != ''
-- ORDER BY tg.global_sales DESC, tg.game_name, tg.year_released;

--
-- 3.3 sale table (M2M)
-- Note: joins on temporary table via name matches resulted in duplicates.
-- Join on game instead and then drop sales columns with an ALTER TABLE statement
-- Without WHERE clauses: 83585 rows in sales (16717 games * 5)
-- Excluding 0.00 sales entries:
-- Total inserts: 56085 rows
--
CREATE TABLE IF NOT EXISTS actor (
  actor_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  actor_name VARCHAR NOT NULL,
  actor_facebook_likes INTEGER NOT NULL,
  PRIMARY KEY (actor_id),
--   FOREIGN KEY (game_id) REFERENCES game(game_id)
--     ON DELETE CASCADE ON UPDATE CASCADE,
--   FOREIGN KEY (region_id) REFERENCES region(region_id)
--     ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO actor
(
actor_id
actor_name
actor_facebook_likes
)
SELECT m.actor_id, 1 as actor_id, g.global_sales AS total_sales
  FROM movie m
 UNION
-- SELECT m.actor_id, 2 as actor_id, g.north_america_sales AS total_sales
--   FROM game g
--  WHERE g.north_america_sales > 0.00
--  UNION
-- SELECT g.game_id, 3 as region_id, g.europe_sales AS total_sales
--   FROM game g
--  WHERE g.europe_sales > 0.00
--  UNION
-- SELECT g.game_id, 4 as region_id, g.japan_sales AS total_sales
--   FROM game g
--  WHERE g.japan_sales > 0.00
--  UNION
-- SELECT g.game_id, 5 as region_id, g.other_sales AS total_sales
--   FROM game g
--  WHERE g.other_sales > 0.00;

--
-- 3.4 temporary numbers table
-- Split comma-delimited developer values in order to populate a developer table
-- and a M2M game_developer associative table
-- Create temporary numbers table that will be used to split out comma-delimited lists of states.
--
CREATE TEMPORARY TABLE numbers
  (
    num INTEGER NOT NULL UNIQUE,
    PRIMARY KEY (num)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO numbers (num) VALUES
  (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15);

--
-- 3.4.1 temp_game_developer
-- Temporary table that stores split out developer companies.
--
CREATE TEMPORARY TABLE temp_game_developer
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    game_id INTEGER NOT NULL,
    developer_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- 3.4.2 This query splits the game developers and inserts them into the target temp table.
-- Note use of DISTINCT.
-- USE TRIM to eliminate white space around developer_name value.
--
INSERT IGNORE INTO temp_game_developer (game_id, developer_name)
SELECT DISTINCT g.game_id,
       TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(g.developer_name, ',', n.num), ',', -1))
       AS developer_name
  FROM numbers n
       INNER JOIN game g
               ON CHAR_LENGTH(g.developer_name) - CHAR_LENGTH(REPLACE(g.developer_name, ',', ''))
                  >= n.num - 1
 ORDER BY g.game_id, developer_name;

--
-- 3.5 developer table
-- Populate with DISTINCT developer_name values from temp_game_developer table
--
CREATE TABLE IF NOT EXISTS developer (
  developer_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  developer_name VARCHAR(100) NOT NULL UNIQUE,
  PRIMARY KEY (developer_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO developer (developer_name)
SELECT DISTINCT TRIM(tgd.developer_name) AS developer_name
  FROM temp_game_developer tgd
 ORDER BY developer_name;

--
-- 3.6 game_developer table (M2M)
-- Insert records from temp_game_developer joined with developer
--
CREATE TABLE IF NOT EXISTS game_developer (
  game_developer_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  game_id INTEGER NOT NULL,
  developer_id INTEGER NOT NULL,
  PRIMARY KEY (game_developer_id),
  FOREIGN KEY (game_id) REFERENCES game(game_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (developer_id) REFERENCES developer(developer_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO game_developer (game_id, developer_id)
SELECT tgd.game_id, d.developer_id
  FROM temp_game_developer tgd
       INNER JOIN developer d
               ON TRIM(tgd.developer_name) = TRIM(d.developer_name)
 ORDER BY tgd.game_id, d.developer_id;

--
-- 4.0 Clean up
--

--
-- 4.1 Drop redundant columns from game table.
--
ALTER TABLE game
      DROP COLUMN north_america_sales,
      DROP COLUMN europe_sales,
      DROP COLUMN japan_sales,
      DROP COLUMN other_sales,
      DROP COLUMN global_sales,
      DROP COLUMN developer_name;

--
-- 4.2 DROP temporary tables
--
DROP TEMPORARY TABLE numbers;
DROP TEMPORARY TABLE temp_game;
DROP TEMPORARY TABLE temp_game_developer;

-- FINIS