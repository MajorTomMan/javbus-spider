package com.javbus.spider.spider.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Question;

@Mapper
public interface SpiderDao {
    void insertQuestion(Question question);

    void deleteQuestionById(int id);

    Question selectQuestionById(int id);

    List<Question> getAllQuestions();

    Question getQuestionByTitle(String title);
}
