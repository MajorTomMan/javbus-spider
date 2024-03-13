package com.javbus.spider.spider.dao.dto;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.dto.ImageDTO;

@Mapper
public interface MovieStarSampleImageDao {
    List<ImageDTO> queryImageDao(Integer movieId);
}
