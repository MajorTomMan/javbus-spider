package com.jav.server.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jav.server.dao.base.DirectorDao;
import com.jav.server.entity.base.Director;
import com.jav.server.service.base.DirectorService;

@Service
public class DirectorServiceImpl implements DirectorService {
    @Autowired
    private DirectorDao directorDao;
    @Override
    public void saveDirector(Director director) {
        // TODO Auto-generated method stub
        directorDao.save(director);
    }
    @Override
    public Director queryDirectorById(Integer id) {
        // TODO Auto-generated method stub
        return directorDao.queryDirectorById(id);
    }
    
}
