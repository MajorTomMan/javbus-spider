package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.javbus.spider.spider.entity.base.Star;

import lombok.Data;

@Data
public class StarCensorVo {
    private List<Star> stars;
    @JsonProperty("is_censored")
    private Boolean isCensored;
}
