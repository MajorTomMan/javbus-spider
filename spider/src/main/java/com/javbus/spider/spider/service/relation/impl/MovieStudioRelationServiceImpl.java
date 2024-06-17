/*
 * @Date: 2024-04-24 20:38:18
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-06-18 00:25:22
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\service\relation\impl\MovieStudioRelationServiceImpl.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 * 
 */
package com.javbus.spider.spider.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.StudioDao;
import com.javbus.spider.spider.dao.relation.MovieStudioDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Studio;
import com.javbus.spider.spider.entity.relation.MovieStudioRelation;
import com.javbus.spider.spider.entity.vo.MovieStudioVO;
import com.javbus.spider.spider.entity.dto.MovieStudioDTO;
import com.javbus.spider.spider.service.relation.MovieStudioRelationService;

@Service
public class MovieStudioRelationServiceImpl implements MovieStudioRelationService {
    @Autowired
    private MovieStudioDao movieStudioDao;
    @Autowired
    private StudioDao studioDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    @Transactional
    public void saveRelation(MovieStudioDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        if (movie == null) {
            movieDao.saveMovie(dto.getMovie());
            movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        } else {
            dto.getMovie().setId(movie.getId());
            movieDao.updateMovie(dto.getMovie());
        }
        Studio studio = studioDao.queryStudioByName(dto.getStudio().getName());
        if (studio == null) {
            studioDao.save(dto.getStudio());
        } else {
            dto.getStudio().setId(studio.getId());
            studioDao.update(dto.getStudio());
        }
        studio = studioDao.queryStudioByName(dto.getStudio().getName());
        MovieStudioRelation movieStudioRelation = movieStudioDao.queryMovieStudioRelation(movie.getId(),
                studio.getId());
        if (movieStudioRelation == null) {
            MovieStudioRelation relation = new MovieStudioRelation();
            relation.setMovieId(movie.getId());
            relation.setStudioId(studio.getId());
            movieStudioDao.addMovieStudioRelation(relation);
        }
    }

    @Override
    public MovieStudioVO queryRelations(Integer movieId) {
        MovieStudioVO vo = new MovieStudioVO();
        Movie movie = movieDao.queryMovieById(movieId);
        vo.setMovie(movie);
        // TODO Auto-generated method stub
        MovieStudioRelation relation = movieStudioDao.queryMovieStudioRelationByMovieId(movieId);
        if (relation == null) {
            return null;
        } else if (relation.getStudioId() == null) {
            vo.setStudio(null);
            return vo;
        }
        Studio studio = studioDao.queryStudioById(relation.getStudioId());
        vo.setStudio(studio);
        return vo;
    }

}
