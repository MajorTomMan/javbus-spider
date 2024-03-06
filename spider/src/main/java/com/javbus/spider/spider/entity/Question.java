package com.javbus.spider.spider.entity;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data
public class Question {

    private int type;

    private int id;

    private int rank;

    private String title;

    private String op1;

    private String op2;

    private String op3;

    private String op4;

    @JsonProperty("titleType")
    private int titleType;

    @JsonProperty("titlePic")
    private String titlePic;

    // Getter and Setter methods
}