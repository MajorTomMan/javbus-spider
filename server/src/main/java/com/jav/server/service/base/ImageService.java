package com.jav.server.service.base;

import java.io.IOException;
import java.util.List;

public interface ImageService {

    List<byte[]> getImagesByCode(String code) throws IOException;

    List<String> queryAllMovieCode(Boolean isCensored, Integer pageSize, Integer offset);
    
}
