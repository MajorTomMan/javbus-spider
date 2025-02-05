package com.jav.server.service.base;

import java.util.List;

import com.jav.server.entity.base.SampleImage;

public interface SampleImageService {

    void saveSampleImages(List<SampleImage> sampleImages);

    SampleImage querySampleImageById(Integer id);

}
