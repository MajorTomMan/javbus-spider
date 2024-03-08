package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.SampleImage;

import lombok.Data;

@Data
public class MovieSampleImageVo {
    private String code;
    private List<SampleImage> sampleImages;
}
