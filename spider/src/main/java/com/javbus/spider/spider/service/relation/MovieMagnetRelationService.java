/*
 * @Date: 2024-05-13 20:52:06
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-05-13 21:00:58
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\service\relation\MovieMagnetRelationService.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */
package com.javbus.spider.spider.service.relation;

import java.util.List;

import com.javbus.spider.spider.entity.dto.MovieMagnetDTO;
import com.javbus.spider.spider.entity.relation.MovieMagnetRelation;

public interface MovieMagnetRelationService {
    void saveRelation(MovieMagnetDTO dto);

    List<MovieMagnetRelation> queryRelationsByMovieId(Integer movieId);

    List<MovieMagnetRelation> queryRelationsByMagnetId(Integer magnetId);
}
