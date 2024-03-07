
DROP DATABASE if EXISTS javbus; 
CREATE DATABASE IF NOT EXISTS javbus CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 切换到 javbus 数据库
USE javbus;

CREATE TABLE IF NOT EXISTS director (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE,
    link VARCHAR(255) UNIQUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS studio (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE,
    link VARCHAR(255) UNIQUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS category (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE,
    link VARCHAR(255) UNIQUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS series (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE,
    link VARCHAR(255) UNIQUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE star(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) ,
    star_link VARCHAR(255) ,
    photo_link VARCHAR(255) ,
    birth_day DATE,
    age INT,
    height VARCHAR(20) ,
    cup VARCHAR(5) ,
    bust VARCHAR(20) ,
    waist VARCHAR(20) ,
    hip VARCHAR(20) ,
    birth_place VARCHAR(255) ,
    hobby VARCHAR(255) 
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS movie (
    id INT PRIMARY KEY AUTO_INCREMENT,
    star_id INT,
    title VARCHAR(255),
    release_date VARCHAR(255),
    length INT,
    link VARCHAR(255),
    director_id INT,
    studio_id INT,
    category_id INT,
    series_id INT,
    FOREIGN KEY (star_id) REFERENCES star(id),
    FOREIGN KEY (director_id) REFERENCES director(id),
    FOREIGN KEY (studio_id) REFERENCES studio(id),
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (series_id) REFERENCES series(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS movie_category_relation (
    movie_id INT,
    category_id INT,
    PRIMARY KEY (movie_id, category_id),
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS movie_star_relation (
    movie_id INT,
    star_id INT,
    PRIMARY KEY (movie_id, star_id),
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (star_id) REFERENCES star(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS star_director_relation (
    star_id INT,
    director_id INT,
    PRIMARY KEY (star_id, director_id),
    FOREIGN KEY (star_id) REFERENCES star(id),
    FOREIGN KEY (director_id) REFERENCES director(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS star_studio_relation (
    star_id INT,
    studio_id INT,
    PRIMARY KEY (star_id, studio_id),
    FOREIGN KEY (star_id) REFERENCES star(id),
    FOREIGN KEY (studio_id) REFERENCES studio(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS star_series_relation (
    star_id INT,
    series_id INT,
    PRIMARY KEY (star_id, series_id),
    FOREIGN KEY (star_id) REFERENCES star(id),
    FOREIGN KEY (series_id) REFERENCES series(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

