package com.jav.server.dao.dto;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.dto.ImageDTO;

import java.util.List;
@Mapper
public interface MovieActressBigImageDao {
    List<ImageDTO> queryImageDao(Integer movieId);
}
