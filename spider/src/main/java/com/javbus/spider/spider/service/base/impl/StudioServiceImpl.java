package com.javbus.spider.spider.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.StudioDao;
import com.javbus.spider.spider.entity.base.Studio;
import com.javbus.spider.spider.service.base.StudioService;

@Service
public class StudioServiceImpl implements StudioService{
    @Autowired
    private StudioDao studioDao;
    @Override
    public void saveStudio(Studio studio) {
        // TODO Auto-generated method stub
        studioDao.save(studio);
    }
    @Override
    public Studio queryStudioById(Integer id) {
        // TODO Auto-generated method stub
        return studioDao.queryStudioById(id);
    }
    @Override
    public Studio queryStudioByName(String name) {
        // TODO Auto-generated method stub
        return studioDao.queryStudioByName(name);
    }
    
}
