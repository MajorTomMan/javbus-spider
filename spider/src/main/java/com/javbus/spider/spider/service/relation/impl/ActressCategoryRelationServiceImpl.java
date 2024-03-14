package com.javbus.spider.spider.service.relation.impl;

import com.javbus.spider.spider.dao.base.CategoryDao;
import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.dao.relation.ActressCategoryDao;
import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.relation.ActressCategoryRelation;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.entity.vo.ActressCategoryVo;
import com.javbus.spider.spider.service.relation.ActressCategoryRelationService;

@Service
public class ActressCategoryRelationServiceImpl implements ActressCategoryRelationService {
    @Autowired
    private ActressCategoryDao ActressCategoryDao;
    @Autowired
    private CategoryDao categoryDao;
    @Autowired
    private ActressDao ActressDao;

    @Override
    public void saveRelation(ActressCategoryVo vo) {
        // TODO Auto-generated method stub
        List<Actress> actresses = vo.getActress();
        List<String> ActressNames = actresses.stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> ActressIds = ActressDao.queryActressIdsByNames(ActressNames);
        if (ActressIds == null || ActressIds.isEmpty()) {
            ActressDao.saveActresses(actresses);
            ActressIds = ActressDao.queryActressIdsByNames(ActressNames);
        }
        List<Category> categories = vo.getCategories();
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
        List<ActressCategoryRelation> ActressCategoryRelations = ActressCategoryDao.queryActressCategoryRelations(ActressIds, categoryIds);
        if(ActressCategoryRelations==null||ActressCategoryRelations.isEmpty()){
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
            ActressCategoryDao.addActressCategoryRelations(relations);
        }

    }

}
