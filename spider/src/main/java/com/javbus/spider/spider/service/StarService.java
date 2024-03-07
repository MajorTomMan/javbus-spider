package com.javbus.spider.spider.service;

import java.util.List;

import com.javbus.spider.spider.entity.Star;

public interface StarService{
    void saveStar(Star star);
    
    void saveStars(List<Star> stars);
}
