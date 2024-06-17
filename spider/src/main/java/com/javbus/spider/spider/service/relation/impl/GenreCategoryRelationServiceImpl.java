package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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
    @Transactional
    public void saveRelation(GenreCategoryDTO dto) {
        // TODO Auto-generated method stub
        Boolean isCensored = dto.getCategories().get(0).getIsCensored();
        Genre genre = genreDao.queryGenreByName(dto.getGenre().getName());
        if (genre == null) {
            genreDao.saveGenre(dto.getGenre());
        } else {
            dto.getGenre().setId(genre.getId());
            genreDao.updateGenre(dto.getGenre());
        }
        genre = genreDao.queryGenreByName(dto.getGenre().getName());
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
        // -------------------------Relations------------------------------
        // 处理有无码的保存问题
        Genre final_genre = genre;
        // 多对一的关系
        List<GenreCategoryRelation> relations = categoryIds.stream().map(id -> {
            GenreCategoryRelation relation = new GenreCategoryRelation();
            relation.setCategoryId(id);
            relation.setGenreId(final_genre.getId());
            return relation;
        }).collect(Collectors.toList());
        if (isCensored) {
            List<GenreCategoryRelation> genreCategoryRelations = genreCategoryDao.queryGenreCategoryCensoredRelations(genre.getId(),
                    categoryIds);
            if (relations.isEmpty()) {
                genreCategoryDao.addGenreCategoryCensoredRelations(genreCategoryRelations);
            } else if (genreCategoryRelations.size() < relations.size()) {
                // 处理新增的关系
                List<GenreCategoryRelation> newRelation = relations.stream().filter(relation -> {
                    return genreCategoryRelations.stream().noneMatch(r -> {
                        return relation.getGenreId() == r.getGenreId() && relation.getCategoryId() == r.getCategoryId();
                    });
                }).toList();
                genreCategoryDao.addGenreCategoryCensoredRelations(newRelation);
            } else {
                genreCategoryDao.updateGenreCategoryCensoredRelations(relations);
            }
        } else {
            List<GenreCategoryRelation> genreCategoryRelations = genreCategoryDao.queryGenreCategoryUncensoredRelations(
                    genre.getId(),categoryIds);
            if (relations.isEmpty()) {
                genreCategoryDao.addGenreCategoryUncensoredRelations(relations);
            } else if (genreCategoryRelations.size() < relations.size()) {
                // 处理新增的关系
                List<GenreCategoryRelation> newRelation = relations.stream().filter(relation -> {
                    return genreCategoryRelations.stream().noneMatch(r -> {
                        return relation.getGenreId() == r.getGenreId() && relation.getCategoryId() == r.getCategoryId();
                    });
                }).toList();
                genreCategoryDao.addGenreCategoryUncensoredRelations(newRelation);
            } else {
                genreCategoryDao.updateGenreCategoryUncensoredRelations(relations);
            }
        }
    }

    @Override
    public GenreCategoryVO queryRelations(Integer genreId) {
        // TODO Auto-generated method stub
        List<GenreCategoryRelation> relations = genreCategoryDao.queryGenreCategoryCensoredRelationsByGenreId(genreId);
        if (relations.isEmpty()) {
            return null;
        }
        Genre genre = genreDao.queryGenreById(genreId);
        List<Integer> categoryIds = relations.stream().map(relation -> {
            return relation.getCategoryId();
        }).collect(Collectors.toList());
        List<Category> categories = categoryDao.queryCategoriesByIds(categoryIds);
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
            if (relations.isEmpty()) {
                return null;
            }
            Genre genre = genreDao.queryGenreById(genreId);
            List<Integer> categoryIds = relations.stream().map(relation -> {
                return relation.getCategoryId();
            }).collect(Collectors.toList());
            List<Category> categories = categoryDao.queryCategoriesByIds(categoryIds);
            GenreCategoryVO vo = new GenreCategoryVO();
            vo.setCategories(categories);
            vo.setGenre(genre);
            return vo;
        }
    }

}
