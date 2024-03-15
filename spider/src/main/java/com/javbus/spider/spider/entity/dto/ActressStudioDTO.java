package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.base.Studio;

import lombok.Data;

@Data
public class ActressStudioDTO {
    private List<Actress> actress;
    private Studio studio;

}
