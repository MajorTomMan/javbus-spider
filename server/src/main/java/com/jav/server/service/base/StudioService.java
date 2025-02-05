package com.jav.server.service.base;

import com.jav.server.entity.base.Studio;

public interface StudioService {

    void saveStudio(Studio studio);

    Studio queryStudioById(Integer id);

    Studio queryStudioByName(String name);
    
}
