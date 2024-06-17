package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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
    @Transactional
    public void saveRelation(MovieCategoryDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        if (movie == null) {
            movieDao.saveMovie(dto.getMovie());
            movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        } else {
            dto.getMovie().setId(movie.getId());
            movieDao.updateMovie(dto.getMovie());
        }
        // -----------------Category-----------------------------
        List<String> categoryNames = dto.getCategories().stream().map((category) -> {
            return category.getName();
        }).collect(Collectors.toList());
        List<Category> categories = categoryDao.queryCategoriesByNames(categoryNames);
        if (categories.isEmpty()) {
            categoryDao.saveCategories(dto.getCategories());
        } else if (categories.size() < dto.getCategories().size()) {
            List<Category> finalCategories = categories;
            List<Category> newCategoryList = dto.getCategories().stream()
                    .filter(category -> {
                        return finalCategories.stream().noneMatch(c -> c.getName().equals(category.getName()));
                    }).toList();
            categoryDao.saveCategories(newCategoryList);
        } else {
            categoryDao.updateCategories(categories);
        }
        categories = categoryDao.queryCategoriesByNames(categoryNames);
        List<Integer> categoryIds = categories.stream().map(category -> category.getId()).collect(Collectors.toList());
        // ---------------------------------Relations------------------------
        final Movie final_movie = movie;
        // 设置一对多关系
        List<MovieCategoryRelation> movieCategoryRelations = movieCategoryDao.queryMovieCategoryRelations(movie.getId(),
                categoryIds);
        List<MovieCategoryRelation> relations = categoryIds.stream().map((id) -> {
            MovieCategoryRelation relation = new MovieCategoryRelation();
            relation.setMovieId(final_movie.getId());
            relation.setCategoryId(id);
            return relation;
        }).collect(Collectors.toList());
        if (movieCategoryRelations.isEmpty()) {
            movieCategoryDao.addMovieCategoryRelations(relations);
        } else if (movieCategoryRelations.size() < relations.size()) {
            List<MovieCategoryRelation> newRelation = relations.stream().filter(relation -> {
                return movieCategoryRelations.stream().noneMatch(r -> {
                    return relation.getCategoryId() == r.getCategoryId() && relation.getMovieId() == r.getMovieId();
                });
            }).toList();
            movieCategoryDao.addMovieCategoryRelations(newRelation);
        } else {
            movieCategoryDao.updateMovieCategoryRelations(relations);
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
        List<Category> categories = categoryDao.queryCategoriesByIds(categoryIds);
        MovieCategoryVO vo = new MovieCategoryVO();
        vo.setCategories(categories);
        vo.setMovie(movie);
        return vo;
    }
}