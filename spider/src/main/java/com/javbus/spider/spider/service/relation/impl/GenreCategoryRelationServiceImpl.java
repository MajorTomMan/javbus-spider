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
        Integer genreId = genreDao.queryGenreIdByName(genre.getName());
        List<Category> categories = dto.getCategories();
        categoryDao.saveCategories(categories);
        List<String> categoryNames = categories.stream().map(category -> {
            return category.getName();
        }).collect(Collectors.toList());
        List<Integer> categoryIds = categoryDao.queryCategoryIdsByNames(categoryNames);
        List<GenreCategoryRelation> genreCategoryRelations = genreCategoryDao.queryGenreCategoryRelations(genreId,
                categoryIds);
        if (genreCategoryRelations == null || genreCategoryRelations.isEmpty()) {
            List<GenreCategoryRelation> relations = categoryIds.stream().map((id) -> {
                GenreCategoryRelation relation = new GenreCategoryRelation();
                relation.setGenreId(genreId);
                relation.setCategoryId(id);
                return relation;
            }).collect(Collectors.toList());
            genreCategoryDao.addGenreCategoryRelations(relations);
        }
    }

    @Override
    public GenreCategoryVO queryRelations(Integer genreId) {
        // TODO Auto-generated method stub
        List<GenreCategoryRelation> relations = genreCategoryDao.queryGenreCategoryRelationsByGenreId(genreId);
        if (relations == null|| relations.isEmpty()) {
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

}
