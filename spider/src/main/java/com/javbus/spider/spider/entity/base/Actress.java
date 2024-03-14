package com.javbus.spider.spider.entity.base;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

/**
 * Actress
 */
@Data
public class Actress {
    private Integer id;
    private String name;
    @JsonProperty("actress_link")
    private String ActressLink;
    @JsonProperty("photo_link")
    private String photoLink;
    @JsonProperty("birth_day")
    private String birthDay;
    private String age;
    private String height;
    private String cup;
    private String bust;
    private String waist;
    private String hip;
    @JsonProperty("birth_place")
    private String birthPlace;
    private String hobby;
    @JsonProperty("is_censored")
    private Boolean isCensored;
}