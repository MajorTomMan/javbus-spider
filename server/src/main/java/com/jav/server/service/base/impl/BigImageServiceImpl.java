package com.jav.server.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jav.server.dao.base.BigImageDao;
import com.jav.server.entity.base.BigImage;
import com.jav.server.service.base.BigImageService;

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
