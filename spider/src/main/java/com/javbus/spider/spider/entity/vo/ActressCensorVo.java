package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class ActressCensorVo {
    private List<Actress> actress;
    @JsonProperty("is_censored")
    private Boolean isCensored;
}
