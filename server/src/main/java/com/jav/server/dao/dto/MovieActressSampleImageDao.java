package com.jav.server.dao.dto;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.dto.ImageDTO;

@Mapper
public interface MovieActressSampleImageDao {
    List<ImageDTO> queryImageDao(Integer movieId);
}
