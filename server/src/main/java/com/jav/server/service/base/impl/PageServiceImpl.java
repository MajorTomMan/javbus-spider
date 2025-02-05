package com.jav.server.service.base.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jav.server.dao.base.ActressDao;
import com.jav.server.dao.base.BigImageDao;
import com.jav.server.dao.base.CategoryDao;
import com.jav.server.dao.base.DirectorDao;
import com.jav.server.dao.base.LabelDao;
import com.jav.server.dao.base.MovieDao;
import com.jav.server.dao.base.SampleImageDao;
import com.jav.server.dao.base.SeriesDao;
import com.jav.server.dao.base.StudioDao;

import com.jav.server.dao.relation.MovieActressDao;
import com.jav.server.dao.relation.MovieBigImageDao;
import com.jav.server.dao.relation.MovieCategoryDao;
import com.jav.server.dao.relation.MovieDirectorDao;
import com.jav.server.dao.relation.MovieLabelDao;
import com.jav.server.dao.relation.MovieSampleImageDao;
import com.jav.server.dao.relation.MovieSeriesDao;
import com.jav.server.dao.relation.MovieStudioDao;
import com.jav.server.entity.base.Actress;
import com.jav.server.entity.base.BigImage;
import com.jav.server.entity.base.Category;
import com.jav.server.entity.base.Director;
import com.jav.server.entity.base.Label;
import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.SampleImage;
import com.jav.server.entity.base.Series;
import com.jav.server.entity.base.Studio;
import com.jav.server.entity.relation.MovieActressRelation;
import com.jav.server.entity.relation.MovieBigImageRelation;
import com.jav.server.entity.relation.MovieCategoryRelation;
import com.jav.server.entity.relation.MovieDirectorRelation;
import com.jav.server.entity.relation.MovieLabelRelation;
import com.jav.server.entity.relation.MovieSampleImageRelation;
import com.jav.server.entity.relation.MovieSeriesRelation;
import com.jav.server.entity.relation.MovieStudioRelation;
import com.jav.server.entity.vo.PageVO;
import com.jav.server.service.base.PageService;

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
            List<Category> categories = categoryDao.queryCategoriesByIds(categoryIds);
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
