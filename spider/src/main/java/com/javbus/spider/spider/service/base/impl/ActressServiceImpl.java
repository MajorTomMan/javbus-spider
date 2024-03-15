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
    private ActressDao actressDao;
    @Override
    public void saveActress(Actress Actress) {
        // TODO Auto-generated method stub
        actressDao.saveActress(Actress);
    }
    @Override
    public void saveActresses(List<Actress> actresses) {
        // TODO Auto-generated method stub
        actressDao.saveActresses(actresses);
    }
    @Override
    public Actress queryActressById(Integer id) {
        // TODO Auto-generated method stub
        return actressDao.queryActressById(id);
    }
    @Override
    public Actress queryActressByName(String name) {
        // TODO Auto-generated method stub
        return actressDao.queryActressByName(name);
    }
}
