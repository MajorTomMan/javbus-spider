package com.javbus.spider.spider.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.SeriesDao;
import com.javbus.spider.spider.entity.base.Series;
import com.javbus.spider.spider.service.base.SeriesService;


@Service
public class SeriesServiceImpl implements SeriesService{
    @Autowired
    private SeriesDao seriesDao;
    @Override
    public void saveSeries(Series series) {
        // TODO Auto-generated method stub
        seriesDao.save(series);
    }
    
}
