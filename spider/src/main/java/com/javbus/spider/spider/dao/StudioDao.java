package com.javbus.spider.spider.dao;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Studio;

@Mapper
public interface StudioDao {
    Studio queryStudioById(Integer id);
    Studio queryStudioByName(Integer id);
    void save(Studio studio);

    void delete(Integer id);

    void update(Studio studio);
}
