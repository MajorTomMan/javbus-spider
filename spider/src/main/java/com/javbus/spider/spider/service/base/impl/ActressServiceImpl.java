package com.javbus.spider.spider.service.base.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.service.base.ActressService;

@Service
public class ActressServiceImpl implements ActressService {
    @Autowired
    private ActressDao ActressDao;
    @Override
    public void saveActress(Actress Actress) {
        // TODO Auto-generated method stub
        ActressDao.saveActress(Actress);
    }
    @Override
    public void saveActresses(List<Actress> actresses) {
        // TODO Auto-generated method stub
        ActressDao.saveActresses(actresses);
    }
    
}
