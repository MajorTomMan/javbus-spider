package com.javbus.spider.spider.entity;

import java.net.URL;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data
public class Movie {
    private Integer id;
    private String title;
    private String code;
    @JsonProperty("release_date")
    private String releaseDate;
    private String length;
    @JsonProperty("big_image_link")
    private String bigImageLink;
    @JsonProperty("sample_image_links")
    private List<String> sampleImageLinks;
    private Label label;
    private Director director;
    private Studio studio;
    private Map<String, URL> stars;
    private Map<String, URL> categories;
    private Series series;
}
