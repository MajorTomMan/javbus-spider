package com.javbus.spider.spider.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.BigImageDao;
import com.javbus.spider.spider.entity.base.BigImage;
import com.javbus.spider.spider.service.base.BigImageService;

@Service
public class BigImageServiceImpl implements BigImageService {
    @Autowired
    private BigImageDao bigImageDao;
    @Override
    public void saveBigImage(BigImage bigImage) {
        // TODO Auto-generated method stub
        bigImageDao.saveBigImage(bigImage);
    }
    @Override
    public BigImage queryBigImageById(Integer id) {
        // TODO Auto-generated method stub
        return bigImageDao.queryBigImageById(id);
    }
    
}
