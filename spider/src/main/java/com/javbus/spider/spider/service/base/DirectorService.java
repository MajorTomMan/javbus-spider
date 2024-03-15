package com.javbus.spider.spider.service.base;

import com.javbus.spider.spider.entity.base.Director;

public interface DirectorService {
    public void saveDirector(Director director);

    public Director queryDirectorById(Integer id);
}
