package com.jav.server.service.base;

import com.jav.server.entity.base.Director;

public interface DirectorService {
    public void saveDirector(Director director);

    public Director queryDirectorById(Integer id);
}
