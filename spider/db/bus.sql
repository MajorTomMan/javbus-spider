-- Active: 1708607962150@@192.168.227.128@3306@javbus

DROP DATABASE if EXISTS javbus; 
CREATE DATABASE IF NOT EXISTS javbus CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 切换到 javbus 数据库
USE javbus;
CREATE TABLE IF NOT EXISTS series (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE,
    link VARCHAR(255) UNIQUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS label (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE,
    link VARCHAR(255) UNIQUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

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



CREATE TABLE star(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE,
    star_link VARCHAR(255) UNIQUE,
    photo_link VARCHAR(255) UNIQUE,
    birth_day DATE,
    age INT,
    height VARCHAR(20),
    cup VARCHAR(5),
    bust VARCHAR(20),
    waist VARCHAR(20),
    hip VARCHAR(20),
    birth_place VARCHAR(255),
    hobby VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS movie (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(255),
    title VARCHAR(255),
    release_date VARCHAR(255),
    length VARCHAR(255),
    link VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE big_image(
    id INT PRIMARY KEY AUTO_INCREMENT,
    movie_id INT,
    link VARCHAR(255),
    FOREIGN KEY (movie_id) REFERENCES movie(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE sample_image(
    id INT PRIMARY KEY AUTO_INCREMENT,
    movie_id INT,
    link VARCHAR(255),
    FOREIGN KEY (movie_id) REFERENCES movie(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS movie_label_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    studio_id INT,
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (studio_id) REFERENCES studio(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS movie_studio_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    studio_id INT,
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (studio_id) REFERENCES studio(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS movie_big_image_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    big_image_id INT,
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (big_image_id) REFERENCES big_image(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS movie_sample_image_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    sample_image_id INT,
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (sample_image_id) REFERENCES sample_image(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS movie_category_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    category_id INT,
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS movie_star_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    star_id INT,
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (star_id) REFERENCES star(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS movie_director_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    director_id INT,
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (director_id) REFERENCES director(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS movie_series_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    series_id INT,
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (series_id) REFERENCES series(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS star_director_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    star_id INT,
    director_id INT,
    FOREIGN KEY (star_id) REFERENCES star(id),
    FOREIGN KEY (director_id) REFERENCES director(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS star_studio_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    star_id INT,
    studio_id INT,
    FOREIGN KEY (star_id) REFERENCES star(id),
    FOREIGN KEY (studio_id) REFERENCES studio(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS star_category_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    star_id INT,
    category_id INT,
    FOREIGN KEY (star_id) REFERENCES star(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS star_series_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    star_id INT,
    series_id INT,
    FOREIGN KEY (star_id) REFERENCES star(id),
    FOREIGN KEY (series_id) REFERENCES series(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
