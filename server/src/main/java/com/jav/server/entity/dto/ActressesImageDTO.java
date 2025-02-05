/*
 * @Date: 2024-04-24 20:38:18
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-05-13 20:34:25
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\entity\dto\ActressesImageDTO.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */

package com.jav.server.entity.dto;

import java.util.List;


import lombok.Data;

@Data
public class ActressesImageDTO {
    private List<String> actresses;
    private List<byte[]> images;
    private List<String> names;
    private String code;
}
