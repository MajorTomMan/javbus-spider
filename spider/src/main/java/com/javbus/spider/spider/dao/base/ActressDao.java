package com.javbus.spider.spider.dao.base;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.base.Actress;

@Mapper
public interface ActressDao {
    void saveActress(Actress actress);

    Integer queryActressIdByName(Integer id);

    Actress queryActressById(Integer id);

    Actress queryActressByName(String name);

    List<Integer> queryActressIdsByNames(List<String> names);

    void update(Actress actress);

    void delete(Integer id);

    void saveActresses(List<Actress> stars);
}
