/*
 * @Date: 2024-05-13 20:45:43
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-05-13 20:56:14
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\entity\relation\MovieMagnetRelation.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */
package com.javbus.spider.spider.entity.relation;

import lombok.Data;

@Data
public class MovieMagnetRelation {
    private Integer id;
    private Integer movieId;
    private Integer magnetId;
}
