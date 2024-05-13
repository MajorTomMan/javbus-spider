package com.javbus.spider.spider.entity.base;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data
public class Magnet {
    private Integer id;
    private String name;
    private String link;
    private String size;
    @JsonProperty("share_date")
    private String shareDate;
}
