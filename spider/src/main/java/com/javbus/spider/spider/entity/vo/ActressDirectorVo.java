package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class ActressDirectorVo {
    private List<Actress> actress;
    private Director director;
}
