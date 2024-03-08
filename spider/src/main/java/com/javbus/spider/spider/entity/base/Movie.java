package com.javbus.spider.spider.entity.base;

import lombok.Data;

@Data
public class Movie {
    private Integer id;
    private String code;
    private String title;
    private String release_date;
    private String length;
    private String link;
}
