package com.javbus.spider.spider.entity;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data
public class QuestionData {

    private int page;

    @JsonProperty("totalCount")
    private int totalCount;

    @JsonProperty("totalPage")
    private int totalPage;

    private int limit;
    @JsonProperty("list")
    private List<Question> questions;

    // Getter and Setter methods
}
