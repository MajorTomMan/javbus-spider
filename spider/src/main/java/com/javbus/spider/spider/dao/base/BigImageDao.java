package com.javbus.spider.spider.dao.base;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.base.BigImage;

@Mapper
public interface BigImageDao {
    // 保存 BigImage 记录
    void saveBigImage(BigImage bigImage);

    // 删除 BigImage 记录
    void deleteBigImage(Integer id);

    // 更新 BigImage 记录
    void updateBigImage(BigImage bigImage);

    // 根据 ID 查询 BigImage 记录
    BigImage queryBigImageById(Integer id);

    BigImage queryBigImageByLink(String link);
}
