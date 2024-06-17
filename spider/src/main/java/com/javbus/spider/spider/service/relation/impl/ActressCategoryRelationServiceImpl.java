package com.javbus.spider.spider.service.relation.impl;

import com.javbus.spider.spider.dao.base.CategoryDao;
import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.dao.relation.ActressCategoryDao;
import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.relation.ActressCategoryRelation;
import com.javbus.spider.spider.entity.vo.ActressCategoryVO;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.javbus.spider.spider.entity.dto.ActressCategoryDTO;
import com.javbus.spider.spider.service.relation.ActressCategoryRelationService;

@Service
public class ActressCategoryRelationServiceImpl implements ActressCategoryRelationService {
    @Autowired
    private ActressCategoryDao actressCategoryDao;
    @Autowired
    private CategoryDao categoryDao;
    @Autowired
    private ActressDao actressDao;

    @Override
    @Transactional
    public void saveRelation(ActressCategoryDTO dto) {
        // TODO Auto-generated method stub
        List<String> actressNames = dto.getActress().stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Actress> actresses = actressDao.queryActressesByNames(actressNames);
        if (actresses.isEmpty()) {
            actressDao.saveActresses(dto.getActress());
        } else if (actresses.size() < actressNames.size()) {
            List<Actress> finalActresses = actresses;
            List<Actress> newActressList = dto.getActress().stream()
                    .filter(actress -> {
                        return finalActresses.stream().noneMatch(a -> a.getName().equals(actress.getName()));
                    }).toList();
            actressDao.saveActresses(newActressList);
        } else {
            actressDao.updateActresses(dto.getActress());
        }
        actresses = actressDao.queryActressesByNames(actressNames);
        List<Integer> actressIds = actresses.stream().map(actress -> actress.getId()).collect(Collectors.toList());
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
        // -------------------Relation-----------------------------
        List<ActressCategoryRelation> actressCategoryRelations = actressCategoryDao
                .queryActressCategoryRelations(
                        actressIds, categoryIds);
        List<ActressCategoryRelation> relations = new ArrayList<>();
        // 处理多对多关系
        for (Integer actressId : actressIds) {
            for (Integer categoryId : categoryIds) {
                ActressCategoryRelation relation = new ActressCategoryRelation();
                relation.setCategoryId(categoryId);
                relation.setActressId(actressId);
                relations.add(relation);
            }
        }
        if (actressCategoryRelations.isEmpty()) {
            actressCategoryDao.addActressCategoryRelations(relations);
        } else if (actressCategoryRelations.size() < relations.size()) {
            // 处理新增的关系
            List<ActressCategoryRelation> newRelation = relations.stream().filter(relation -> {
                return actressCategoryRelations.stream().noneMatch(r -> {
                    return relation.getActressId() == r.getActressId() && relation.getCategoryId() == r.getCategoryId();
                });
            }).toList();
            actressCategoryDao.addActressCategoryRelations(newRelation);
        } else {
            actressCategoryDao.updateActressCategoryRelations(relations);
        }
    }

    @Override
    public ActressCategoryVO queryRelations(Integer actressId) {
        // TODO Auto-generated method stub
        List<ActressCategoryRelation> relations = actressCategoryDao
                .queryActressCategoryRelationsByActressId(actressId);
        if (relations == null || relations.isEmpty()) {
            return null;
        }
        Actress actress = actressDao.queryActressById(actressId);
        List<Integer> categoryIds = relations.stream().map(relation -> {
            return relation.getCategoryId();
        }).collect(Collectors.toList());
        List<Category> categories = categoryDao.queryCategoriesByIds(categoryIds);
        ActressCategoryVO vo = new ActressCategoryVO();
        vo.setActress(actress);
        vo.setCategories(categories);
        return vo;
    }

}
