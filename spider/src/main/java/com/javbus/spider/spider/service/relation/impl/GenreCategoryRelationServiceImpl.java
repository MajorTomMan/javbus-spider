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
        Boolean isCensored = dto.getCategories().get(0).getIsCensored();
        Genre genre = genreDao.queryGenreByName(dto.getGenre().getName());
        if (genre == null) {
            genreDao.saveGenre(genre);
            genre = genreDao.queryGenreByName(dto.getGenre().getName());
        }
        List<Category> categories = dto.getCategories();
        List<String> names = categories.stream().map((category) -> {
            return category.getName();
        }).collect(Collectors.toList());
        List<Integer> categoryIds = categoryDao.queryCategoryIdsByNames(names);
        if (categoryIds.isEmpty()) {
            categoryDao.saveCategories(categories);
            categoryIds = categoryDao.queryCategoryIdsByNames(names);
        } else {
            for(int i=0;i<=categoryIds.size();i++){
                dto.getCategories().get(i).setId(categoryIds.get(i));
            }
            categoryDao.updateCategories(dto.getCategories());
        }
        // 处理有无码的保存问题
        final Genre final_genre = genre;
        List<GenreCategoryRelation> genreCategoryRelations = categoryIds.stream().map(id -> {
            GenreCategoryRelation relation = new GenreCategoryRelation();
            relation.setCategoryId(id);
            relation.setGenreId(final_genre.getId());
            return relation;
        }).collect(Collectors.toList());
        if (isCensored) {
            List<GenreCategoryRelation> relations = genreCategoryDao.queryGenreCategoryCensoredRelations(genre.getId(),
                    categoryIds);
            if (relations.isEmpty()) {
                genreCategoryDao.addGenreCategoryCensoredRelations(genreCategoryRelations);
            } else {
                genreCategoryDao.updateGenreCategoryCensoredRelations(genreCategoryRelations);
            }
        } else {
            List<GenreCategoryRelation> relations = genreCategoryDao.queryGenreCategoryUncensoredRelations(genre.getId(),
                    categoryIds);
            if (relations.isEmpty()) {
                genreCategoryDao.addGenreCategoryUncensoredRelations(genreCategoryRelations);
            } else {
                genreCategoryDao.updateGenreCategoryUncensoredRelations(genreCategoryRelations);
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
