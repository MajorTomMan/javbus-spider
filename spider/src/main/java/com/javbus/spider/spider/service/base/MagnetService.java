/*
 * @Date: 2024-05-12 16:02:55
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-05-13 20:48:16
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\service\base\MagnetService.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */
package com.javbus.spider.spider.service.base;

import java.util.List;

import com.javbus.spider.spider.entity.base.Magnet;

public interface MagnetService {
    void save(Magnet magnet);

    void delete(Integer id);

    void update(Magnet magnet);

    Magnet getById(Integer id);

    Magnet getByLink(String link);

    List<Magnet> getByLinks(List<String> links);

    List<Integer> getIdsByLinks(List<String> links);

}
