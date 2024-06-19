-- Active: 1688392670869@@192.168.253.131@3306@javbus
DROP DATABASE if EXISTS javbus;

CREATE DATABASE IF NOT EXISTS javbus CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- 切换到 javbus 数据库
USE javbus;

CREATE TABLE IF NOT EXISTS series (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(255) COMMENT '名称',
    link VARCHAR(255) COMMENT '链接'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '系列表';

CREATE TABLE IF NOT EXISTS genre (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(255) COMMENT '名称'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '类型表';

CREATE TABLE IF NOT EXISTS label (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(255) COMMENT '名称',
    link VARCHAR(255) COMMENT '链接'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '发行商表';

CREATE TABLE IF NOT EXISTS director (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(255) COMMENT '名称',
    link VARCHAR(255) COMMENT '链接'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '导演表';

CREATE TABLE IF NOT EXISTS studio (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(255) COMMENT '名称',
    link VARCHAR(255) COMMENT '链接'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '制作商表';

CREATE TABLE IF NOT EXISTS category (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(255) COMMENT '名称',
    link VARCHAR(255) COMMENT '链接',
    is_censored BOOLEAN COMMENT '是否有码'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '分类表';

CREATE TABLE actress (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(255) COMMENT '名称',
    actress_link VARCHAR(255) COMMENT '链接',
    photo_link VARCHAR(255) COMMENT '照片链接',
    birth_day DATE COMMENT '生日',
    age INT COMMENT '年龄',
    height VARCHAR(20) COMMENT '身高',
    cup VARCHAR(5) COMMENT '罩杯',
    bust VARCHAR(20) COMMENT '胸围',
    waist VARCHAR(20) COMMENT '腰围',
    hip VARCHAR(20) COMMENT '臀围',
    birth_place VARCHAR(255) COMMENT '出生地',
    hobby VARCHAR(255) COMMENT '爱好',
    is_censored BOOLEAN COMMENT '是否有码'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '女优表';

CREATE TABLE IF NOT EXISTS movie (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    code VARCHAR(255) COMMENT '代码',
    title VARCHAR(255) COMMENT '标题',
    release_date VARCHAR(255) COMMENT '发布日期',
    length VARCHAR(255) COMMENT '长度',
    link VARCHAR(255) COMMENT '链接',
    is_censored BOOLEAN COMMENT '是否有码'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '电影表';

CREATE TABLE big_image (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    link VARCHAR(255) COMMENT '链接'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '封面表';

CREATE TABLE sample_image (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    link VARCHAR(255) COMMENT '链接'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '样品图像表';

CREATE TABLE magnet (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    name VARCHAR(255),
    link VARCHAR(255) COMMENT '链接',
    size VARCHAR(255),
    share_date VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '磁力链接表';

CREATE TABLE IF NOT EXISTS movie_label_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    movie_id INT COMMENT '电影ID',
    label_id INT COMMENT '发行商ID',
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    FOREIGN KEY (label_id) REFERENCES label (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '电影-发行商关系表';

CREATE TABLE IF NOT EXISTS movie_studio_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    movie_id INT COMMENT '电影ID',
    studio_id INT COMMENT '制作商ID',
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    FOREIGN KEY (studio_id) REFERENCES studio (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '电影-制作商关系表';

CREATE TABLE IF NOT EXISTS movie_big_image_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    movie_id INT COMMENT '电影ID',
    big_image_id INT COMMENT '封面ID',
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    FOREIGN KEY (big_image_id) REFERENCES big_image (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '电影-封面关系表';

CREATE TABLE IF NOT EXISTS movie_sample_image_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    movie_id INT COMMENT '电影ID',
    sample_image_id INT COMMENT '样品图像ID',
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    FOREIGN KEY (sample_image_id) REFERENCES sample_image (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '电影-样品图像关系表';

CREATE TABLE IF NOT EXISTS movie_category_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    movie_id INT COMMENT '电影ID',
    category_id INT COMMENT '分类ID',
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    FOREIGN KEY (category_id) REFERENCES category (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '电影-分类关系表';

CREATE TABLE IF NOT EXISTS movie_actress_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    movie_id INT COMMENT '电影ID',
    actress_id INT COMMENT '女优ID',
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    FOREIGN KEY (actress_id) REFERENCES actress (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '电影-女优关系表';

CREATE TABLE IF NOT EXISTS movie_director_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    movie_id INT COMMENT '电影ID',
    director_id INT COMMENT '导演ID',
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    FOREIGN KEY (director_id) REFERENCES director (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '电影-导演关系表';

CREATE TABLE IF NOT EXISTS movie_series_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    movie_id INT COMMENT '电影ID',
    series_id INT COMMENT '系列ID',
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    FOREIGN KEY (series_id) REFERENCES series (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '电影-系列关系表';

CREATE TABLE IF NOT EXISTS actress_director_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    actress_id INT COMMENT '女优ID',
    director_id INT COMMENT '导演ID',
    FOREIGN KEY (actress_id) REFERENCES actress (id),
    FOREIGN KEY (director_id) REFERENCES director (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '女优-导演关系表';

CREATE TABLE IF NOT EXISTS actress_studio_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    actress_id INT COMMENT '女优ID',
    studio_id INT COMMENT '制作商ID',
    FOREIGN KEY (actress_id) REFERENCES actress (id),
    FOREIGN KEY (studio_id) REFERENCES studio (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '女优-制作商关系表';

CREATE TABLE IF NOT EXISTS actress_category_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    actress_id INT COMMENT '女优ID',
    category_id INT COMMENT '分类ID',
    FOREIGN KEY (actress_id) REFERENCES actress (id),
    FOREIGN KEY (category_id) REFERENCES category (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '女优-分类关系表';

CREATE TABLE IF NOT EXISTS actress_series_relation (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    actress_id INT COMMENT '女优ID',
    series_id INT COMMENT '系列ID',
    FOREIGN KEY (actress_id) REFERENCES actress (id),
    FOREIGN KEY (series_id) REFERENCES series (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '女优-系列关系表';

CREATE TABLE IF NOT EXISTS genre_category_censored_relation (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    genre_id INT COMMENT '类型ID',
    category_id INT COMMENT '分类ID',
    FOREIGN KEY (genre_id) REFERENCES genre (id),
    FOREIGN KEY (category_id) REFERENCES category (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '类型-分类关系表';

CREATE TABLE IF NOT EXISTS genre_category_uncensored_relation (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    genre_id INT COMMENT '类型ID',
    category_id INT COMMENT '分类ID',
    FOREIGN KEY (genre_id) REFERENCES genre (id),
    FOREIGN KEY (category_id) REFERENCES category (id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '类型-分类关系表';

CREATE TABLE movie_magnet_relation (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    movie_id INT COMMENT '类型ID',
    magnet_id INT COMMENT '磁力ID',
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (magnet_id) REFERENCES magnet(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '影片-磁力关系表';
-- 对于 movie_label_relation 表
ALTER TABLE movie_label_relation
ADD FOREIGN KEY (movie_id) REFERENCES movie (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 movie_studio_relation 表
ALTER TABLE movie_studio_relation
ADD FOREIGN KEY (movie_id) REFERENCES movie (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 movie_big_image_relation 表
ALTER TABLE movie_big_image_relation
ADD FOREIGN KEY (movie_id) REFERENCES movie (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 movie_sample_image_relation 表
ALTER TABLE movie_sample_image_relation
ADD FOREIGN KEY (movie_id) REFERENCES movie (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 movie_category_relation 表
ALTER TABLE movie_category_relation
ADD FOREIGN KEY (movie_id) REFERENCES movie (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 movie_actress_relation 表
ALTER TABLE movie_actress_relation
ADD FOREIGN KEY (movie_id) REFERENCES movie (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 movie_director_relation 表
ALTER TABLE movie_director_relation
ADD FOREIGN KEY (movie_id) REFERENCES movie (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 movie_series_relation 表
ALTER TABLE movie_series_relation
ADD FOREIGN KEY (movie_id) REFERENCES movie (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 actress_director_relation 表
ALTER TABLE actress_director_relation
ADD FOREIGN KEY (actress_id) REFERENCES actress (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 actress_studio_relation 表
ALTER TABLE actress_studio_relation
ADD FOREIGN KEY (actress_id) REFERENCES actress (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 actress_category_relation 表
ALTER TABLE actress_category_relation
ADD FOREIGN KEY (actress_id) REFERENCES actress (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 actress_series_relation 表
ALTER TABLE actress_series_relation
ADD FOREIGN KEY (actress_id) REFERENCES actress (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 genre_category_censored_relation 表
ALTER TABLE genre_category_censored_relation
ADD FOREIGN KEY (genre_id) REFERENCES genre (id) ON DELETE CASCADE ON UPDATE CASCADE;
-- 对于 genre_category_uncensored_relation 表
ALTER TABLE genre_category_uncensored_relation
ADD FOREIGN KEY (genre_id) REFERENCES genre (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE movie_magnet_relation
ADD FOREIGN KEY (movie_id) REFERENCES  movie(id) ON DELETE CASCADE ON UPDATE CASCADE;