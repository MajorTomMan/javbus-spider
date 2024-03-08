package com.javbus.spider.spider.service.base;

import java.util.List;

import com.javbus.spider.spider.entity.base.Star;

public interface StarService{
    void saveStar(Star star);
    
    void saveStars(List<Star> stars);
}
