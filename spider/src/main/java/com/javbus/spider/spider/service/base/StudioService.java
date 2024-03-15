package com.javbus.spider.spider.service.base;

import com.javbus.spider.spider.entity.base.Studio;

public interface StudioService {

    void saveStudio(Studio studio);

    Studio queryStudioById(Integer id);

    Studio queryStudioByName(String name);
    
}
