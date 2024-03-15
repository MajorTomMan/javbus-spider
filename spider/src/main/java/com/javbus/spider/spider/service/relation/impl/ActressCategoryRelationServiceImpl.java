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
    public void saveRelation(ActressCategoryDTO dto) {
        // TODO Auto-generated method stub
        List<Actress> actresses = dto.getActress();
        List<String> ActressNames = actresses.stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> ActressIds = actressDao.queryActressIdsByNames(ActressNames);
        if (ActressIds == null || ActressIds.isEmpty()) {
            actressDao.saveActresses(actresses);
            ActressIds = actressDao.queryActressIdsByNames(ActressNames);
        }
        List<Category> categories = dto.getCategories();
        // 先保存进数据库保证数据存在
        categoryDao.saveCategories(categories);
        List<String> categoryNames = categories.stream().map((category) -> {
            return category.getName();
        }).collect(Collectors.toList());
        List<Integer> categoryIds = categoryDao.queryCategoryIdsByNames(categoryNames);
        if (categoryIds == null || categoryIds.isEmpty()) {
            categoryDao.saveCategories(categories);
            categoryIds = categoryDao.queryCategoryIdsByNames(categoryNames);
        }
        List<ActressCategoryRelation> ActressCategoryRelations = actressCategoryDao
                .queryActressCategoryRelations(ActressIds, categoryIds);
        if (ActressCategoryRelations == null || ActressCategoryRelations.isEmpty()) {
            List<ActressCategoryRelation> relations = new ArrayList<>();
            // 处理多对多关系
            for (Integer actressId : ActressIds) {
                for (Integer categoryId : categoryIds) {
                    ActressCategoryRelation relation = new ActressCategoryRelation();
                    relation.setCategoryId(categoryId);
                    relation.setActressId(actressId);
                    relations.add(relation);
                }
            }
            actressCategoryDao.addActressCategoryRelations(relations);
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
        List<Category> categories = categoryDao.queryCategories(categoryIds);
        ActressCategoryVO vo = new ActressCategoryVO();
        vo.setActress(actress);
        vo.setCategories(categories);
        return vo;
    }

}
