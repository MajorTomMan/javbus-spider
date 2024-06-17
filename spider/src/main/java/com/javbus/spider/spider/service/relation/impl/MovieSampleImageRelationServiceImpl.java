/*
 * @Date: 2024-04-24 20:38:18
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-06-18 00:25:05
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\service\relation\impl\MovieSampleImageRelationServiceImpl.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 * 
 */
package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.SampleImageDao;
import com.javbus.spider.spider.dao.relation.MovieSampleImageDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.SampleImage;
import com.javbus.spider.spider.entity.relation.MovieSampleImageRelation;
import com.javbus.spider.spider.entity.vo.MovieSampleImageVO;
import com.javbus.spider.spider.entity.dto.MovieSampleImageDTO;
import com.javbus.spider.spider.service.relation.MovieSampleImageRelationService;

@Service
public class MovieSampleImageRelationServiceImpl implements MovieSampleImageRelationService {
    @Autowired
    private MovieSampleImageDao movieSampleImageDao;
    @Autowired
    private SampleImageDao sampleImageDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    @Transactional
    public void saveRelation(MovieSampleImageDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        if (movie == null) {
            movieDao.saveMovie(dto.getMovie());
        } else {
            dto.getMovie().setId(movie.getId());
            movieDao.updateMovie(dto.getMovie());
        }
        movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        // --------------------Sample Image ---------------------------
        List<SampleImage> sampleImages = sampleImageDao
                .querySampleImageByLinks(dto.getSampleImages().stream().map(sample -> sample.getLink()).toList());
        if (sampleImages.isEmpty()) {
            sampleImageDao.saveSampleImages(sampleImages);
        } else if (sampleImages.size() <= dto.getSampleImages().size()) {
            List<SampleImage> finalSampleImages = sampleImages;
            List<SampleImage> newSampleImages = dto.getSampleImages().stream().filter(sample -> {
                return finalSampleImages.stream().noneMatch(s -> s.getLink().equals(sample.getLink()));
            }).toList();
            sampleImageDao.saveSampleImages(newSampleImages);
        } else {
            sampleImageDao.updateSampleImages(sampleImages);
        }
        sampleImages = sampleImageDao
                .querySampleImageByLinks(dto.getSampleImages().stream().map(sample -> sample.getLink()).toList());
        List<Integer> sampleImageIds = sampleImageDao
                .querySampleImageIdsByLinks(dto.getSampleImages().stream().map(sample -> sample.getLink()).toList());
        // -------------------Relations--------------------------
        List<MovieSampleImageRelation> movieSampleImageRelations = movieSampleImageDao
                .queryMovieSampleImageRelations(movie.getId(), sampleImageIds);
        final Movie final_movie = movie;
        List<MovieSampleImageRelation> relations = sampleImageIds.stream().map((id) -> {
            MovieSampleImageRelation relation = new MovieSampleImageRelation();
            relation.setMovieId(final_movie.getId());
            relation.setSampleImageId(id);
            return relation;
        }).collect(Collectors.toList());
        if (movieSampleImageRelations.isEmpty()) {
            movieSampleImageDao.addMovieSampleImageRelations(relations);
        } else if (movieSampleImageRelations.size() < relations.size()) {
            List<MovieSampleImageRelation> newRelation = relations.stream().filter(relation -> {
                return movieSampleImageRelations.stream().noneMatch(r -> {
                    return relation.getSampleImageId() == r.getSampleImageId()
                            && relation.getMovieId() == r.getMovieId();
                });
            }).toList();
            movieSampleImageDao.addMovieSampleImageRelations(newRelation);
        } else {
            movieSampleImageDao.updateMovieSampleImageRelations(relations);
        }
    }

    @Override
    public MovieSampleImageVO queryRelations(Integer movieId) {
        // TODO Auto-generated method stub
        List<MovieSampleImageRelation> relations = movieSampleImageDao.queryMovieSampleImageRelationsByMovieId(movieId);
        if (relations == null || relations.isEmpty()) {
            return null;
        }
        Movie movie = movieDao.queryMovieById(movieId);
        List<Integer> sampleImageIds = relations.stream().map(relation -> {
            return relation.getSampleImageId();
        }).collect(Collectors.toList());
        List<SampleImage> sampleImages = sampleImageDao.querySampleImagesByIds(sampleImageIds);
        MovieSampleImageVO vo = new MovieSampleImageVO();
        vo.setMovie(movie);
        vo.setSampleImages(sampleImages);
        return vo;
    }

}
