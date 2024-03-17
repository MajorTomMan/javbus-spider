package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.CategoryDao;
import com.javbus.spider.spider.dao.base.GenreDao;
import com.javbus.spider.spider.dao.relation.GenreCategoryDao;
import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Genre;
import com.javbus.spider.spider.entity.relation.GenreCategoryRelation;
import com.javbus.spider.spider.entity.vo.GenreCategoryVO;
import com.javbus.spider.spider.entity.dto.GenreCategoryDTO;
import com.javbus.spider.spider.service.relation.GenreCategoryRelationService;

@Service
public class GenreCategoryRelationServiceImpl implements GenreCategoryRelationService {
    @Autowired
    private GenreCategoryDao genreCategoryDao;
    @Autowired
    private CategoryDao categoryDao;
    @Autowired
    private GenreDao genreDao;

    @Override
    public void saveRelation(GenreCategoryDTO dto) {
        // TODO Auto-generated method stub
        Genre genre = dto.getGenre();
        genreDao.saveGenre(dto.getGenre());
        categoryDao.saveCategories(dto.getCategories());
        Integer genreId = genreDao.queryGenreIdByName(genre.getName());
        Boolean isCensored = dto.getCategories().get(0).getIsCensored();
        List<String> categoryNames = dto.getCategories().stream().map(category -> {
            return category.getName();
        }).collect(Collectors.toList());
        List<Integer> categoryIds = categoryDao.queryCategoryIdsByNames(categoryNames);
        if (isCensored) {
            List<GenreCategoryRelation> genreCategoryRelations = genreCategoryDao.queryGenreCategoryCensoredRelations(
                    genreId,
                    categoryIds);
            if (genreCategoryRelations == null || genreCategoryRelations.isEmpty()) {
                List<GenreCategoryRelation> relations = categoryIds.stream().map((id) -> {
                    GenreCategoryRelation relation = new GenreCategoryRelation();
                    relation.setGenreId(genreId);
                    relation.setCategoryId(id);
                    return relation;
                }).collect(Collectors.toList());
                genreCategoryDao.addGenreCategoryCensoredRelations(relations);
            }
        } else {
            List<GenreCategoryRelation> genreCategoryRelations = genreCategoryDao.queryGenreCategoryUncensoredRelations(
                    genreId,
                    categoryIds);
            if (genreCategoryRelations == null || genreCategoryRelations.isEmpty()) {
                List<GenreCategoryRelation> relations = categoryIds.stream().map((id) -> {
                    GenreCategoryRelation relation = new GenreCategoryRelation();
                    relation.setGenreId(genreId);
                    relation.setCategoryId(id);
                    return relation;
                }).collect(Collectors.toList());
                genreCategoryDao.addGenreCategoryUncensoredRelations(relations);
            }
        }
    }

    @Override
    public GenreCategoryVO queryRelations(Integer genreId) {
        // TODO Auto-generated method stub
        List<GenreCategoryRelation> relations = genreCategoryDao.queryGenreCategoryCensoredRelationsByGenreId(genreId);
        if (relations == null || relations.isEmpty()) {
            return null;
        }
        Genre genre = genreDao.queryGenreById(genreId);
        List<Integer> categoryIds = relations.stream().map(relation -> {
            return relation.getCategoryId();
        }).collect(Collectors.toList());
        List<Category> categories = categoryDao.queryCategories(categoryIds);
        GenreCategoryVO vo = new GenreCategoryVO();
        vo.setCategories(categories);
        vo.setGenre(genre);
        return vo;
    }

    @Override
    public GenreCategoryVO queryRelations(Integer genreId, Boolean isCensored) {
        // TODO Auto-generated method stub
        if (isCensored) {
            return queryRelations(genreId);
        } else {
            List<GenreCategoryRelation> relations = genreCategoryDao
                    .queryGenreCategoryUncensoredRelationsByGenreId(genreId);
            Genre genre = genreDao.queryGenreById(genreId);
            List<Integer> categoryIds = relations.stream().map(relation -> {
                return relation.getCategoryId();
            }).collect(Collectors.toList());
            List<Category> categories = categoryDao.queryCategories(categoryIds);
            GenreCategoryVO vo = new GenreCategoryVO();
            vo.setCategories(categories);
            vo.setGenre(genre);
            return vo;
        }
    }

}
