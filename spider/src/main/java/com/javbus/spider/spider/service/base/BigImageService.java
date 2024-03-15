package com.javbus.spider.spider.service.base;

import com.javbus.spider.spider.entity.base.BigImage;

public interface BigImageService {

    void saveBigImage(BigImage bigImage);

    BigImage queryBigImageById(Integer id);

}
