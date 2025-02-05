package com.jav.server.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jav.server.dao.base.LabelDao;
import com.jav.server.entity.base.Label;
import com.jav.server.service.base.LabelService;

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
