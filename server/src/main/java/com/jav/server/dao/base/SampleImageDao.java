package com.jav.server.dao.base;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.base.SampleImage;

@Mapper
public interface SampleImageDao {
    SampleImage querySampleImageById(Integer id);

    void saveSampleImages(List<SampleImage> sampleImages);

    List<Integer> querySampleImageIdsByLinks(List<String> links);

    List<SampleImage> querySampleImageByLinks(List<String> links);

    List<SampleImage> querySampleImagesByIds(List<Integer> sampleImageIds);

    void updateSampleImage(SampleImage sampleImage);
    void updateSampleImages(List<SampleImage> sampleImages);
}
