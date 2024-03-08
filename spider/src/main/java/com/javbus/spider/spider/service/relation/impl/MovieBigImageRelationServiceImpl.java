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
public class MovieBigImageRelationServiceImpl implements MovieBigImageRelationService{
    @Autowired
    private MovieBigImageDao movieBigImageDao;
    @Autowired
    private MovieDao movieDao;
    @Autowired
    private BigImageDao bigImageDao;
    @Override
    public void saveRelaton(MovieBigImageVo vo) {
        // TODO Auto-generated method stub
        MovieBigImageRelation relation = new MovieBigImageRelation();
        Movie movie = movieDao.queryMovieByCode(vo.getCode());
        if(movie==null){
            return;
        }
        BigImage bigImage = vo.getBigImage();
        BigImage bigImageResult = bigImageDao.queryBigImageByLink(bigImage.getLink());
        if(bigImageResult==null){
            bigImageDao.saveBigImage(bigImage);
            bigImage=bigImageDao.queryBigImageByLink(vo.getBigImage().getLink());
        }
        relation.setBigImageId(bigImageResult.getId());
        relation.setMovieId(movie.getId());
        movieBigImageDao.addMovieBigImageRelation(relation);
    }
    
}
