package com.javbus.spider.spider.service.base.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.SampleImageDao;
import com.javbus.spider.spider.entity.base.SampleImage;
import com.javbus.spider.spider.service.base.SampleImageService;

@Service
public class SampleImageServiceImpl implements SampleImageService{
    @Autowired
    private SampleImageDao sampleImageDao;
    @Override
    public void saveSampleImages(List<SampleImage> sampleImages) {
        // TODO Auto-generated method stub
        sampleImageDao.saveSampleImages(sampleImages);
    }
    
}
