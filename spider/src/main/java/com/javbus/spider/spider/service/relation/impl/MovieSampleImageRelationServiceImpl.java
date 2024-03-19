package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.SampleImageDao;
import com.javbus.spider.spider.dao.dto.MovieActressSampleImageDao;
import com.javbus.spider.spider.dao.relation.MovieSampleImageDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.SampleImage;
import com.javbus.spider.spider.entity.relation.MovieSampleImageRelation;
import com.javbus.spider.spider.entity.vo.MovieSampleImageVO;
import com.javbus.spider.spider.entity.dto.MovieSampleImageDTO;
import com.javbus.spider.spider.service.relation.MovieSampleImageRelationService;
import com.javbus.spider.spider.utils.ImageUtil;

@Service
public class MovieSampleImageRelationServiceImpl implements MovieSampleImageRelationService {
    @Autowired
    private MovieActressSampleImageDao movieActressSampleImageDao;
    @Autowired
    private MovieSampleImageDao movieSampleImageDao;
    @Autowired
    private SampleImageDao sampleImageDao;
    @Autowired
    private MovieDao movieDao;
    @Autowired
    private ImageUtil imageUtil;

    @Override
    public void saveRelation(MovieSampleImageDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByCode(dto.getMovie().getCode());
        if (movie != null) {
            movieDao.updateMovieByCode(dto.getMovie());
        } else {
            movieDao.saveMovie(dto.getMovie());
            movie = movieDao.queryMovieByCode(dto.getMovie().getCode());
        }
        List<Integer> sampleImageIds = sampleImageDao.querySampleImageIdsByLinks(dto.getSampleImages());
        if (sampleImageIds.isEmpty() || sampleImageIds.size() != dto.getSampleImages().size()) {
            sampleImageDao.saveSampleImages(dto.getSampleImages());
            sampleImageIds = sampleImageDao.querySampleImageIdsByLinks(dto.getSampleImages());
        } else {
            for (int i = 0; i < sampleImageIds.size(); i++) {
                dto.getSampleImages().get(i).setId(sampleImageIds.get(i));
            }
            sampleImageDao.updateSampleImages(dto.getSampleImages());
        }
        List<MovieSampleImageRelation> movieSampleImageRelations = movieSampleImageDao
                .queryMovieSampleImageRelations(movie.getId(), sampleImageIds);
        if (movieSampleImageRelations.isEmpty()) {
            final Movie final_movie = movie;
            List<MovieSampleImageRelation> relations = sampleImageIds.stream().map((id) -> {
                MovieSampleImageRelation relation = new MovieSampleImageRelation();
                relation.setMovieId(final_movie.getId());
                relation.setSampleImageId(id);
                return relation;
            }).collect(Collectors.toList());
            movieSampleImageDao.addMovieSampleImageRelations(relations);
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
