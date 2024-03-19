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
import com.javbus.spider.spider.entity.vo.MovieCategoryVO;
import com.javbus.spider.spider.entity.dto.MovieCategoryDTO;
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
    public void saveRelation(MovieCategoryDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByCode(dto.getMovie().getCode());
        if (movie != null) {
            movieDao.updateMovieByCode(dto.getMovie());
        } else {
            movieDao.saveMovie(dto.getMovie());
            movie = movieDao.queryMovieByCode(dto.getMovie().getCode());
        }
        // 根据名字查找ID
        List<String> names = dto.getCategories().stream().map((data) -> {
            return data.getName();
        }).collect(Collectors.toList());
        List<Integer> categoryIds = categoryDao.queryCategoryIdsByNames(names);
        if(categoryIds.isEmpty()){
            categoryDao.saveCategories(dto.getCategories());
            categoryIds = categoryDao.queryCategoryIdsByNames(names);
        }
        else{
            for(int i=0;i<=categoryIds.size();i++){
                dto.getCategories().get(i).setId(categoryIds.get(i));
            }
            categoryDao.updateCategories(dto.getCategories());
        }
        final Movie final_movie = movie;
        // 设置一对多关系
        List<MovieCategoryRelation> movieCategoryRelations = movieCategoryDao.queryMovieCategoryRelations(movie.getId(),
                categoryIds);
        if (movieCategoryRelations.isEmpty()) {
            List<MovieCategoryRelation> relations = categoryIds.stream().map((id) -> {
                MovieCategoryRelation relation = new MovieCategoryRelation();
                relation.setMovieId(final_movie.getId());
                relation.setCategoryId(id);
                return relation;
            }).collect(Collectors.toList());
            movieCategoryDao.addMovieCategoryRelations(relations);
        }
    }

    @Override
    public MovieCategoryVO queryRelations(Integer movieId) {
        // TODO Auto-generated method stub
        List<MovieCategoryRelation> relations = movieCategoryDao.queryMovieCategoryRelationsByMovieId(movieId);
        if (relations == null || relations.isEmpty()) {
            return null;
        }
        Movie movie = movieDao.queryMovieById(movieId);
        List<Integer> categoryIds = relations.stream().map(relation -> {
            return relation.getCategoryId();
        }).collect(Collectors.toList());
        List<Category> categories = categoryDao.queryCategories(categoryIds);
        MovieCategoryVO vo = new MovieCategoryVO();
        vo.setCategories(categories);
        vo.setMovie(movie);
        return vo;
    }
}