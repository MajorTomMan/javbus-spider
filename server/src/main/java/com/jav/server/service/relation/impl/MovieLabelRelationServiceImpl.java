/*
 * @Date: 2024-04-24 20:38:18
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-06-18 00:24:39
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\service\relation\impl\MovieLabelRelationServiceImpl.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */
package com.jav.server.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.jav.server.dao.base.LabelDao;
import com.jav.server.dao.base.MovieDao;
import com.jav.server.dao.relation.MovieLabelDao;
import com.jav.server.entity.base.Label;
import com.jav.server.entity.base.Movie;
import com.jav.server.entity.relation.MovieLabelRelation;
import com.jav.server.entity.vo.MovieLabelVO;
import com.jav.server.entity.dto.MovieLabelDTO;
import com.jav.server.service.relation.MovieLabelRelationService;

@Service
public class MovieLabelRelationServiceImpl implements MovieLabelRelationService {
    @Autowired
    private MovieLabelDao movieLabelDao;
    @Autowired
    private LabelDao labelDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    @Transactional
    public void saveRelation(MovieLabelDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        if (movie == null) {
            movieDao.saveMovie(dto.getMovie());
            movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        } else {
            dto.getMovie().setId(movie.getId());
            movieDao.updateMovie(dto.getMovie());
        }
        Label label = labelDao.queryLabelByName(dto.getLabel().getName());
        if (label == null) {
            labelDao.save(dto.getLabel());
            label = labelDao.queryLabelByName(dto.getLabel().getName());
        } else {
            dto.getLabel().setId(label.getId());
            labelDao.update(dto.getLabel());
        }
        MovieLabelRelation movieLabelRelation = movieLabelDao.queryMovieLabelRelation(movie.getId(), label.getId());
        if (movieLabelRelation == null) {
            MovieLabelRelation relation = new MovieLabelRelation();
            relation.setLabelId(label.getId());
            relation.setMovieId(movie.getId());
            movieLabelDao.addMovieLabelRelation(relation);
        }

    }

    @Override
    public MovieLabelVO queryRelations(Integer movieId) {
        // TODO Auto-generated method stub
        MovieLabelRelation relation = movieLabelDao.queryMovieLabelRelationByMovieId(movieId);
        if (relation == null) {
            return null;
        }
        MovieLabelVO vo = new MovieLabelVO();
        Movie movie = movieDao.queryMovieById(movieId);
        vo.setMovie(movie);
        Label label = labelDao.queryLabelById(relation.getLabelId());
        vo.setLabel(label);
        return vo;
    }

}
