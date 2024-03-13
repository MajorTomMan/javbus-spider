package com.javbus.spider.spider.entity.dto;

import lombok.Data;

@Data
public class BigImageDTO {
    // 女优名字
    private String name;
    // 番号
    private String code;
    private String fileName;
    private byte[] bigImage;
}
