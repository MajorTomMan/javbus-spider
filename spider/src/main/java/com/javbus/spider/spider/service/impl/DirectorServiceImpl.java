package com.javbus.spider.spider.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.DirectorDao;
import com.javbus.spider.spider.entity.Director;
import com.javbus.spider.spider.service.DirectorService;

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
