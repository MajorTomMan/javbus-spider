package com.jav.server.dao.base;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.base.Director;

@Mapper
public interface DirectorDao {
    void save(Director director);
    Director queryDirectorById(Integer id);
    Director queryDirectorByName(String name);
    void update(Director director);
    void delete(Integer id);
}
