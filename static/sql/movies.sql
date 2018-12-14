-- Data set: https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings (22 Dec 2016)

--
-- 1.0 Setup. Delete tables after every build iteration.
--
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS movie, keyword, country, director,movie_language, actor, genre, rating, temp_director;
SET FOREIGN_KEY_CHECKS=1;

--
-- 2.0 ENTITIES
-- Serve as lookup tables
--

--
-- 2.1 unique table
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
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n' 
  IGNORE 1 LINES
  (genre_name);

CREATE TABLE IF NOT EXISTS country (
  country_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  country_name VARCHAR(25) NOT NULL UNIQUE,
  PRIMARY KEY (country_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movies/zfp-country.csv'
INTO TABLE country
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (country_name);  

CREATE TABLE IF NOT EXISTS temp_director (
  director_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  movie_title VARCHAR(500) NOT NULL,
  director_name VARCHAR(250) NOT NULL,
  director_facebook_likes VARCHAR(500) NULL,
  PRIMARY KEY (director_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movies/zfp-directors.csv'
INTO TABLE temp_director
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (movie_title, director_name, director_facebook_likes);  

CREATE TABLE IF NOT EXISTS keyword (
  keyword_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  keyword_name VARCHAR(100) NOT NULL UNIQUE,
  PRIMARY KEY (keyword_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movies/zfp-keywords_unique.csv'
INTO TABLE keyword
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (keyword_name); 

CREATE TABLE IF NOT EXISTS movie_language (
  language_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  language_name VARCHAR(25) NOT NULL UNIQUE,
  PRIMARY KEY (language_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movies/zfp-language.csv'
INTO TABLE movie_language
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (language_name); 

CREATE TABLE IF NOT EXISTS rating (
  rating_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  rating VARCHAR(25) NOT NULL UNIQUE,
  PRIMARY KEY (rating_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/movies/zfp-rating.csv'
INTO TABLE rating
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (rating); 