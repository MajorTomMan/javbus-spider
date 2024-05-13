/*
 * @Date: 2024-05-12 16:05:01
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-05-13 21:44:01
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\dao\base\MagnetDao.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */
package com.javbus.spider.spider.dao.base;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.base.Magnet;

@Mapper
public interface MagnetDao {
    void saveMagnet(Magnet magnet);

    void saveMagnets(List<Magnet> magnets);

    // 删除 Magnet 记录
    void deleteMagnet(Integer id);

    // 更新 Magnet 记录
    void updateMagnet(Magnet magnet);

    // 根据 ID 查询 Magnet 记录
    Magnet queryMagnetById(Integer id);

    Magnet queryMagnetByLink(String link);

    List<Magnet> queryMagnets(List<String> links);

    List<Integer> queryMagnetIdsByLinks(List<String> links);
}
