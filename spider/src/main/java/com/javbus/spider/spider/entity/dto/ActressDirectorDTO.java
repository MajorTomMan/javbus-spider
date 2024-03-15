package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class ActressDirectorDTO {
    private List<Actress> actress;
    private Director director;
}
