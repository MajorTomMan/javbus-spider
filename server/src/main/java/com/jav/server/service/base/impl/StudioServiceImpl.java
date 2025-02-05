package com.jav.server.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jav.server.dao.base.StudioDao;
import com.jav.server.entity.base.Studio;
import com.jav.server.service.base.StudioService;

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
