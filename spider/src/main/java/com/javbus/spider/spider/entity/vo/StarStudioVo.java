package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Star;
import com.javbus.spider.spider.entity.base.Studio;

import lombok.Data;

@Data
public class StarStudioVo {
    private List<Star> stars;
    private Studio studio;

}
