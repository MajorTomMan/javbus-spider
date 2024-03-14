package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.base.Studio;

import lombok.Data;

@Data
public class ActressStudioVo {
    private List<Actress> actress;
    private Studio studio;

}
