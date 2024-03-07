package com.javbus.spider.spider.entity.request;

import java.net.URL;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.javbus.spider.spider.entity.Category;
import com.javbus.spider.spider.entity.Director;
import com.javbus.spider.spider.entity.Label;
import com.javbus.spider.spider.entity.Series;
import com.javbus.spider.spider.entity.Star;
import com.javbus.spider.spider.entity.Studio;

import lombok.Data;

@Data
public class MovieRequest {
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
    private List<Star>  stars;
    private List<Category> categories;
    private Series series;
}
