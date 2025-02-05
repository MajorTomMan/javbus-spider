/*
 * @Date: 2024-04-24 20:38:18
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-04-24 20:44:43
 * @FilePath: \Python\JavBus\spider\src\main\java\com\javbus\spider\spider\service\relation\impl\MovieBigImageRelationServiceImpl.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */
package com.jav.server.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.jav.server.dao.base.BigImageDao;
import com.jav.server.dao.base.MovieDao;
import com.jav.server.dao.relation.MovieBigImageDao;
import com.jav.server.entity.base.BigImage;
import com.jav.server.entity.base.Movie;
import com.jav.server.entity.relation.MovieBigImageRelation;
import com.jav.server.entity.vo.MovieBigImageVO;
import com.jav.server.entity.dto.MovieBigImageDTO;
import com.jav.server.service.relation.MovieBigImageRelationService;

@Service
public class MovieBigImageRelationServiceImpl implements MovieBigImageRelationService {
    @Autowired
    private MovieBigImageDao movieBigImageDao;
    @Autowired
    private MovieDao movieDao;
    @Autowired
    private BigImageDao bigImageDao;

    @Override
    @Transactional
    public void saveRelaton(MovieBigImageDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        if (movie == null) {
            movieDao.saveMovie(dto.getMovie());
        } else {
            dto.getMovie().setId(movie.getId());
            movieDao.updateMovie(dto.getMovie());
        }
        movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        BigImage bigImage = bigImageDao.queryBigImageByLink(dto.getBigImage().getLink());
        if (bigImage == null) {
            bigImageDao.saveBigImage(dto.getBigImage());
        } else {
            dto.getBigImage().setId(bigImage.getId());
            bigImageDao.updateBigImage(dto.getBigImage());
        }
        bigImage = bigImageDao.queryBigImageByLink(dto.getBigImage().getLink());
        MovieBigImageRelation movieBigImageRelation = movieBigImageDao.queryMovieBigImageRelation(movie.getId(),
                bigImage.getId());
        if (movieBigImageRelation == null) {
            MovieBigImageRelation relation = new MovieBigImageRelation();
            relation.setBigImageId(bigImage.getId());
            relation.setMovieId(movie.getId());
            movieBigImageDao.addMovieBigImageRelation(relation);
        }
    }

    @Override
    public MovieBigImageVO queryRelations(Integer movieId) {
        // TODO Auto-generated method stub
        MovieBigImageRelation relation = movieBigImageDao.queryMovieBigImageRelationByMovieId(movieId);
        if (relation == null) {
            return null;
        }
        Movie movie = movieDao.queryMovieById(relation.getMovieId());
        BigImage BigImage = bigImageDao.queryBigImageById(relation.getBigImageId());
        MovieBigImageVO vo = new MovieBigImageVO();
        vo.setBigImage(BigImage);
        vo.setMovie(movie);
        return vo;
    }

}
