package com.javbus.spider.spider.entity;

import lombok.Data;

@Data
public class Movie {
    private Integer id;
    private Integer star_id;
    private String title;
    private String release_date;
    private Integer length;
    private String link;
    private Integer director_id;
    private Integer studio_id;
    private Integer category_id;
    private Integer series_id;
}
