package com.jav.server.service.base;

import com.jav.server.entity.base.BigImage;

public interface BigImageService {

    void saveBigImage(BigImage bigImage);

    BigImage queryBigImageById(Integer id);

}
