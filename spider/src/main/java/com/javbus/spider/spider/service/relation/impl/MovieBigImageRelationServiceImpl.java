package com.javbus.spider.spider.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.BigImageDao;
import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.relation.MovieBigImageDao;
import com.javbus.spider.spider.entity.base.BigImage;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.relation.MovieBigImageRelation;
import com.javbus.spider.spider.entity.vo.MovieBigImageVo;
import com.javbus.spider.spider.service.relation.MovieBigImageRelationService;

@Service
public class MovieBigImageRelationServiceImpl implements MovieBigImageRelationService {
    @Autowired
    private MovieBigImageDao movieBigImageDao;
    @Autowired
    private MovieDao movieDao;
    @Autowired
    private BigImageDao bigImageDao;

    @Override
    public void saveRelaton(MovieBigImageVo vo) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        if (movie == null) {
            movieDao.saveMovie(vo.getMovie());
            movie=movieDao.queryMovieByCode(vo.getMovie().getCode());
        }
        BigImage bigImage = vo.getBigImage();
        BigImage bigImageResult = bigImageDao.queryBigImageByLink(bigImage.getLink());
        if (bigImageResult == null) {
            bigImageDao.saveBigImage(bigImage);
            bigImageResult = bigImageDao.queryBigImageByLink(vo.getBigImage().getLink());
        }
        MovieBigImageRelation relation = new MovieBigImageRelation();
        relation.setBigImageId(bigImageResult.getId());
        relation.setMovieId(movie.getId());
        movieBigImageDao.addMovieBigImageRelation(relation);
    }

}
