package com.javbus.spider.spider.service.base;

import java.util.List;

import com.javbus.spider.spider.entity.base.Actress;

public interface ActressService{
    void saveActress(Actress actress);
    
    void saveActresses(List<Actress> stars);
}
