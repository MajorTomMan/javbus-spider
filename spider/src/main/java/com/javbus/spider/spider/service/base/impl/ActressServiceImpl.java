package com.javbus.spider.spider.service.base.impl;

import java.util.List;
import java.util.stream.Collectors;

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
    public void saveActress(Actress actress) {
        // TODO Auto-generated method stub
        Actress act = actressDao.queryActressByName(actress.getName());
        if (act == null) {
            actressDao.saveActress(actress);
        } else {
            actress.setId(act.getId());
            actressDao.update(actress);
        }
    }

    @Override
    public void saveActresses(List<Actress> actresses) {
        // TODO Auto-generated method stub
        List<String> names = actresses.stream().map(actress -> {
            return actress.getName();
        }).collect(Collectors.toList());
        List<Integer> ids = actressDao.queryActressIdsByNames(names);
        if (ids.isEmpty() || ids.size() != actresses.size()) {
            actressDao.saveActresses(actresses);
        } else {
            for (int i = 0; i < ids.size(); i++) {
                actresses.get(i).setId(ids.get(i));
            }
            actressDao.updateActresses(actresses);
        }
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
