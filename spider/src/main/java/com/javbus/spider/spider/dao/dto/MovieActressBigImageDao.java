package com.javbus.spider.spider.dao.dto;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.dto.ImageDTO;

import java.util.List;
@Mapper
public interface MovieActressBigImageDao {
    List<ImageDTO> queryImageDao(Integer movieId);
}
