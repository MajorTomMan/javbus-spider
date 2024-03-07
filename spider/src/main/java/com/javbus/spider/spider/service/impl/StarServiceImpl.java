package com.javbus.spider.spider.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.StarDao;
import com.javbus.spider.spider.entity.Star;
import com.javbus.spider.spider.service.StarService;

@Service
public class StarServiceImpl implements StarService {
    @Autowired
    private StarDao starDao;
    @Override
    public void saveStar(Star star) {
        // TODO Auto-generated method stub
        starDao.save(star);
    }
    
}
