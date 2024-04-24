
package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class ActressesImageDTO {
    private List<Actress> actresses;
    private List<byte[]> images;
    private List<String> names;
    private String code;
}
