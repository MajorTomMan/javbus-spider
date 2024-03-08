package com.javbus.spider.spider.dao.base;

import java.util.List;

import com.javbus.spider.spider.entity.base.SampleImage;

public interface SampleImageDao {
    SampleImage querySampleImageById(Integer id);

    void saveSampleImages(List<SampleImage> sampleImages);

    List<Integer> querySampleImageIdsByLinks(List<SampleImage> sampleImages);
}
