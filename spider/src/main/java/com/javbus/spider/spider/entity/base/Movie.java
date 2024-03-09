package com.javbus.spider.spider.entity.base;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data
public class Movie {
    private Integer id;
    private String code;
    private String title;
    @JsonProperty("release_date")
    private String releaseDate;
    private String length;
    private String link;
}
