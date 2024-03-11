package com.javbus.spider.spider.service.base.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.StarDao;
import com.javbus.spider.spider.entity.base.Star;
import com.javbus.spider.spider.service.base.StarService;

@Service
public class StarServiceImpl implements StarService {
    @Autowired
    private StarDao starDao;
    @Override
    public void saveStar(Star star) {
        // TODO Auto-generated method stub
        starDao.saveStar(star);
    }
    @Override
    public void saveStars(List<Star> stars) {
        // TODO Auto-generated method stub
        starDao.saveStars(stars);
    }
    
}
