package com.jav.server.service.base.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jav.server.dao.base.SampleImageDao;
import com.jav.server.entity.base.SampleImage;
import com.jav.server.service.base.SampleImageService;

@Service
public class SampleImageServiceImpl implements SampleImageService{
    @Autowired
    private SampleImageDao sampleImageDao;
    @Override
    public void saveSampleImages(List<SampleImage> sampleImages) {
        // TODO Auto-generated method stub
        sampleImageDao.saveSampleImages(sampleImages);
    }
    @Override
    public SampleImage querySampleImageById(Integer id) {
        // TODO Auto-generated method stub
        return sampleImageDao.querySampleImageById(id);
    }
    
}
