package com.javbus.spider.spider.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.DirectorDao;
import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.service.base.DirectorService;

@Service
public class DirectorServiceImpl implements DirectorService {
    @Autowired
    private DirectorDao directorDao;
    @Override
    public void saveDirector(Director director) {
        // TODO Auto-generated method stub
        directorDao.save(director);
    }
    
}
