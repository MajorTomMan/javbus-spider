package com.jav.server.entity.base;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data
public class Category {
    private Integer id;
    private String name;
    private String link;
    @JsonProperty("is_censored")
    private Boolean isCensored;
}
