package com.javbus.spider.spider.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.StudioDao;
import com.javbus.spider.spider.entity.Studio;
import com.javbus.spider.spider.service.StudioService;

@Service
public class StudioServiceImpl implements StudioService{
    @Autowired
    private StudioDao studioDao;
    @Override
    public void saveStudio(Studio studio) {
        // TODO Auto-generated method stub
        studioDao.save(studio);
    }
    
}
