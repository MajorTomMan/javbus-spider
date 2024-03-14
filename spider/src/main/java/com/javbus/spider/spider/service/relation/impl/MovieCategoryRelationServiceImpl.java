package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.CategoryDao;
import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.relation.MovieCategoryDao;
import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.relation.MovieCategoryRelation;
import com.javbus.spider.spider.entity.vo.MovieCategoryVo;
import com.javbus.spider.spider.service.relation.MovieCategoryRelationService;


@Service
public class MovieCategoryRelationServiceImpl implements MovieCategoryRelationService {
    @Autowired
    private MovieCategoryDao movieCategoryDao;
    @Autowired
    private CategoryDao categoryDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    public void saveRelation(MovieCategoryVo vo) {
        // TODO Auto-generated method stub
        movieDao.saveMovie(vo.getMovie());
        categoryDao.saveCategories(vo.getCategories());
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        List<Category> categories = vo.getCategories();
        // 根据名字查找ID
        List<String> names = categories.stream().map((data) -> {
            return data.getName();
        }).collect(Collectors.toList());
        List<Integer> categoryIds = categoryDao.queryCategoryIdsByNames(names);
        final Movie final_movie=movie;
        // 设置一对多关系
        List<MovieCategoryRelation> movieCategoryRelations = movieCategoryDao.queryMovieCategoryRelations(movie.getId(), categoryIds);
        if(movieCategoryRelations==null|| movieCategoryRelations.isEmpty()){
            List<MovieCategoryRelation> relations = categoryIds.stream().map((id) -> {
                MovieCategoryRelation relation = new MovieCategoryRelation();
                relation.setMovieId(final_movie.getId());
                relation.setCategoryId(id);
                return relation;
            }).collect(Collectors.toList());
            movieCategoryDao.addMovieCategoryRelations(relations);
        }
    }
}