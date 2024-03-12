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
import com.javbus.spider.spider.entity.vo.GenreCategoryVo;
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
    public void saveRelation(GenreCategoryVo vo) {
        // TODO Auto-generated method stub
        Genre genre = vo.getGenre();
        genreDao.saveGenre(vo.getGenre());
        Integer genreid = genreDao.queryGenreIdByName(genre.getName());
        List<Category> categories = vo.getCategories();
        categoryDao.saveCategories(categories);
        List<String> categoryNames = categories.stream().map(category -> {
            return category.getName();
        }).collect(Collectors.toList());
        List<Integer> categoryIds = categoryDao.queryCategoryIdsByNames(categoryNames);
        
        List<GenreCategoryRelation> relations = categoryIds.stream().map((id) -> {
            GenreCategoryRelation relation = new GenreCategoryRelation();
            relation.setGenreId(genreid);
            relation.setCategoryId(id);
            return relation;
        }).collect(Collectors.toList());
        genreCategoryDao.addGenreCategoryRelations(relations);
    }

}
