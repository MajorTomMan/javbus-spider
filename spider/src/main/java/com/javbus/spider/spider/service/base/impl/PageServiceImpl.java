package com.javbus.spider.spider.service.base.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.dao.base.BigImageDao;
import com.javbus.spider.spider.dao.base.CategoryDao;
import com.javbus.spider.spider.dao.base.DirectorDao;
import com.javbus.spider.spider.dao.base.LabelDao;
import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.SampleImageDao;
import com.javbus.spider.spider.dao.base.SeriesDao;
import com.javbus.spider.spider.dao.base.StudioDao;

import com.javbus.spider.spider.dao.relation.MovieActressDao;
import com.javbus.spider.spider.dao.relation.MovieBigImageDao;
import com.javbus.spider.spider.dao.relation.MovieCategoryDao;
import com.javbus.spider.spider.dao.relation.MovieDirectorDao;
import com.javbus.spider.spider.dao.relation.MovieLabelDao;
import com.javbus.spider.spider.dao.relation.MovieSampleImageDao;
import com.javbus.spider.spider.dao.relation.MovieSeriesDao;
import com.javbus.spider.spider.dao.relation.MovieStudioDao;
import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.base.BigImage;
import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.base.Label;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.SampleImage;
import com.javbus.spider.spider.entity.base.Series;
import com.javbus.spider.spider.entity.base.Studio;
import com.javbus.spider.spider.entity.relation.MovieActressRelation;
import com.javbus.spider.spider.entity.relation.MovieBigImageRelation;
import com.javbus.spider.spider.entity.relation.MovieCategoryRelation;
import com.javbus.spider.spider.entity.relation.MovieDirectorRelation;
import com.javbus.spider.spider.entity.relation.MovieLabelRelation;
import com.javbus.spider.spider.entity.relation.MovieSampleImageRelation;
import com.javbus.spider.spider.entity.relation.MovieSeriesRelation;
import com.javbus.spider.spider.entity.relation.MovieStudioRelation;
import com.javbus.spider.spider.entity.vo.PageVO;
import com.javbus.spider.spider.service.base.PageService;

@Service
public class PageServiceImpl implements PageService {
    @Autowired
    private MovieStudioDao movieStudioDao;
    @Autowired
    private MovieSeriesDao movieSeriesDao;
    @Autowired
    private MovieLabelDao movieLabelDao;
    @Autowired
    private MovieBigImageDao movieBigImageDao;
    @Autowired
    private MovieSampleImageDao movieSampleImageDao;
    @Autowired
    private MovieActressDao movieActressDao;
    @Autowired
    private MovieDirectorDao movieDirectorDao;
    @Autowired
    private MovieCategoryDao movieCategoryDao;
    @Autowired
    private SampleImageDao sampleImageDao;
    @Autowired
    private SeriesDao seriesDao;
    @Autowired
    private BigImageDao bigImageDao;
    @Autowired
    private CategoryDao categoryDao;
    @Autowired
    private StudioDao studioDao;
    @Autowired
    private LabelDao labelDao;
    @Autowired
    private DirectorDao directorDao;
    @Autowired
    private ActressDao actressDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    public PageVO queryPageByMovieId(Integer movieId) {
        // TODO Auto-generated method stub
        PageVO vo = new PageVO();
        Movie movie = movieDao.queryMovieById(movieId);
        vo.setMovie(movie);
        List<MovieActressRelation> movieActressRelations = movieActressDao.queryMovieActressRelationByMovieId(movieId);
        if (movieActressRelations == null || movieActressRelations.isEmpty()) {
            vo.setActresses(null);
        } else {
            List<Integer> actressIds = movieActressRelations.stream().map(relation -> {
                return relation.getActressId();
            }).collect(Collectors.toList());
            List<Actress> actresses = actressDao.queryActressesById(actressIds);
            if (actresses.isEmpty()) {
                vo.setActresses(null);
            } else {
                vo.setActresses(actresses);
            }
        }
        MovieDirectorRelation movieDirectorRelation = movieDirectorDao.queryMovieDirectorRelationByMovieId(movieId);
        if (movieDirectorRelation == null) {
            vo.setDirector(null);
        } else {
            Director director = directorDao.queryDirectorById(movieDirectorRelation.getDirectorId());
            vo.setDirector(director);
        }
        MovieStudioRelation movieStudioRelation = movieStudioDao.queryMovieStudioRelationByMovieId(movieId);
        if (movieStudioRelation == null) {
            vo.setStudio(null);
        } else {
            Studio studio = studioDao.queryStudioById(movieStudioRelation.getStudioId());
            vo.setStudio(studio);
        }

        MovieSeriesRelation movieSeriesRelation = movieSeriesDao.queryMovieSeriesRelationByMovieId(movieId);
        if (movieSeriesRelation == null) {
            vo.setSeries(null);
        } else {
            Series series = seriesDao.querySeriesById(movieSeriesRelation.getSeriesId());
            vo.setSeries(series);
        }
        MovieLabelRelation movieLabelRelation = movieLabelDao.queryMovieLabelRelationByMovieId(movieId);
        if (movieLabelRelation == null) {
            vo.setLabel(null);
        } else {
            Label label = labelDao.queryLabelById(movieLabelRelation.getLabelId());
            vo.setLabel(label);
        }

        MovieBigImageRelation movieBigImageRelation = movieBigImageDao.queryMovieBigImageRelationByMovieId(movieId);
        if (movieBigImageRelation == null) {
            vo.setBigImage(null);
        } else {
            BigImage bigImage = bigImageDao.queryBigImageById(movieBigImageRelation.getBigImageId());
            vo.setBigImage(bigImage);
        }
        List<MovieCategoryRelation> movieCategoryRelations = movieCategoryDao
                .queryMovieCategoryRelationsByMovieId(movieId);
        if (movieCategoryRelations == null || movieCategoryRelations.isEmpty()) {
            vo.setCategories(null);
        } else {
            List<Integer> categoryIds = movieCategoryRelations.stream().map(relation -> {
                return relation.getCategoryId();
            }).collect(Collectors.toList());
            List<Category> categories = categoryDao.queryCategories(categoryIds);
            vo.setCategories(categories);
        }
        List<MovieSampleImageRelation> movieSampleImageRelations = movieSampleImageDao
                .queryMovieSampleImageRelationsByMovieId(movieId);
        if (movieSampleImageRelations == null || movieSampleImageRelations.isEmpty()) {
            vo.setSampleImages(null);
        } else {
            List<Integer> sampleImageIds = movieSampleImageRelations.stream().map(relation -> {
                return relation.getSampleImageId();
            }).collect(Collectors.toList());
            List<SampleImage> sampleImages = sampleImageDao.querySampleImagesByIds(sampleImageIds);
            vo.setSampleImages(sampleImages);
        }
        return vo;
    }
}
