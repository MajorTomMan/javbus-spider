/*
 * @Author: hujunhao hujunhao@rtczsz.com
 * @Date: 2024-04-13 14:03:54
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-04-16 23:35:34
 * @FilePath: \Python\JavBus\spider\src\main\java\com\javbus\spider\spider\entity\dto\ActressesImageDTO.java
 * @Description: Test
 * 
 * Copyright (c) 2024 by rtcz.com, All Rights Reserved. 
 */
package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class ActressesImageDTO {
    private List<Actress> actresses;
    private List<byte[]> bytes;
    private List<String> fileNames;
    private String code;
}
