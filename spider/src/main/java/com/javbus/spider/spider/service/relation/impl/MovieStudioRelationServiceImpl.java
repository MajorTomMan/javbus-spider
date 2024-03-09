package com.javbus.spider.spider.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.StudioDao;
import com.javbus.spider.spider.dao.relation.MovieStudioDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Studio;
import com.javbus.spider.spider.entity.relation.MovieStudioRelation;
import com.javbus.spider.spider.entity.vo.MovieStudioVo;
import com.javbus.spider.spider.service.relation.MovieStudioRelationService;


@Service
public class MovieStudioRelationServiceImpl implements MovieStudioRelationService{
    @Autowired
    private MovieStudioDao movieStudioDao;
    @Autowired
    private StudioDao studioDao;
    @Autowired
    private MovieDao movieDao;
    @Override
    public void saveRelation(MovieStudioVo vo) {
        // TODO Auto-generated method stub
        if(vo==null){
            return;
        }
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        if(movie==null){
            return;
        }
        Studio studio = studioDao.queryStudioByName(vo.getStudio().getName());
        if(studio==null){
            studioDao.save(vo.getStudio());
            studio = studioDao.queryStudioByName(vo.getStudio().getName());
        }
        MovieStudioRelation relation = new MovieStudioRelation();
        relation.setMovieId(movie.getId());
        relation.setStudioId(studio.getId());
        movieStudioDao.addMovieStudioRelation(relation);
    }
    
}
