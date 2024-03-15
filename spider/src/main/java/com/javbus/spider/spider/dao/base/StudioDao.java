package com.javbus.spider.spider.dao.base;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.base.Studio;

@Mapper
public interface StudioDao {
    Studio queryStudioById(Integer id);
    Studio queryStudioByName(String name);
    List<Studio> queryStudioByIds(List<Integer> ids);
    void save(Studio studio);

    void delete(Integer id);

    void update(Studio studio);
}
