package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.SampleImage;

import lombok.Data;

@Data
public class MovieSampleImageVO {
    Movie movie;
    List<SampleImage> sampleImages;
}
