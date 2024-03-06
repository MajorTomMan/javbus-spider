-- Active: 1708607962150@@192.168.227.128@3306
-- 创建 driver_exam 数据库
CREATE DATABASE IF NOT EXISTS driver_exam CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 切换到 driver_exam 数据库
USE driver_exam;

-- 创建 question 表
CREATE TABLE IF NOT EXISTS question (
    question_id INT PRIMARY KEY,
    question_type INT,
    question_rank INT,
    title VARCHAR(255),
    op1 VARCHAR(255),
    op2 VARCHAR(255),
    op3 VARCHAR(255),
    op4 VARCHAR(255),
    titleType INT,
    titlePic VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;