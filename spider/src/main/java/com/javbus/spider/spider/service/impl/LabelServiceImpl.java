package com.javbus.spider.spider.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.LabelDao;
import com.javbus.spider.spider.entity.Label;
import com.javbus.spider.spider.service.LabelService;

@Service
public class LabelServiceImpl implements LabelService{
    @Autowired
    private LabelDao labelDao;
    @Override
    public void saveLabel(Label label) {
        // TODO Auto-generated method stub
        labelDao.save(label);
    }
    
}
