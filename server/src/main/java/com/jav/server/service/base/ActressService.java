package com.jav.server.service.base;

import java.util.List;

import com.jav.server.entity.base.Actress;

public interface ActressService{
    void saveActress(Actress actress);
    
    void saveActresses(List<Actress> stars);

    Actress queryActressById(Integer id);

    Actress queryActressByName(String name);

    List<String> queryActresses(Integer offset);
}
