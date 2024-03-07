package com.javbus.spider.spider.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.SeriesDao;
import com.javbus.spider.spider.entity.Series;
import com.javbus.spider.spider.service.SeriesService;

@Service
public class SeriesServiceImpl implements SeriesService{
    @Autowired 
    SeriesDao seriesDao;
    @Override
    public void saveSeries(Series series) {
        // TODO Auto-generated method stub
        seriesDao.save(series);
    }
    
}
