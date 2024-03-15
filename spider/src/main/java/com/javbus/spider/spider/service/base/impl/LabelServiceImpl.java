package com.javbus.spider.spider.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.LabelDao;
import com.javbus.spider.spider.entity.base.Label;
import com.javbus.spider.spider.service.base.LabelService;

@Service
public class LabelServiceImpl implements LabelService{
    @Autowired
    private LabelDao labelDao;
    @Override
    public void saveLabel(Label label) {
        // TODO Auto-generated method stub
        labelDao.save(label);
    }
    @Override
    public Label queryLabelById(Integer id) {
        // TODO Auto-generated method stub
        return labelDao.queryLabelById(id);
    }
    @Override
    public Label queryLabelByName(String name) {
        // TODO Auto-generated method stub
        return labelDao.queryLabelByName(name);
    }
}
