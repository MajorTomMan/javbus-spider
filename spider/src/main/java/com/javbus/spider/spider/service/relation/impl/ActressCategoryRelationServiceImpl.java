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
        List<String> actressNames = dto.getActress().stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> actressIds = actressDao.queryActressIdsByNames(actressNames);
        if (actressIds.isEmpty() || actressIds.size() != dto.getActress().size()) {
            actressDao.saveActresses(dto.getActress());
            actressIds = actressDao.queryActressIdsByNames(actressNames);
        } else {
            for (int i = 0; i < actressIds.size(); i++) {
                dto.getActress().get(i).setId(actressIds.get(i));
            }
            actressDao.updateActresses(dto.getActress());
        }
        List<String> categoryNames = dto.getCategories().stream().map((category) -> {
            return category.getName();
        }).collect(Collectors.toList());
        List<Integer> categoryIds = categoryDao.queryCategoryIdsByNames(categoryNames);
        // 先保存进数据库保证数据存在
        if (categoryIds.isEmpty() || categoryIds.size() != dto.getCategories().size()) {
            categoryDao.saveCategories(dto.getCategories());
            categoryIds = categoryDao.queryCategoryIdsByNames(categoryNames);
        } else {
            for (int i = 0; i < categoryIds.size(); i++) {
                dto.getCategories().get(i).setId(categoryIds.get(i));
            }
            categoryDao.updateCategories(dto.getCategories());
        }
        List<ActressCategoryRelation> actressCategoryRelations = actressCategoryDao
                .queryActressCategoryRelations(actressIds, categoryIds);
        if (actressCategoryRelations.isEmpty()) {
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
        List<Category> categories = categoryDao.queryCategoriesByIds(categoryIds);
        ActressCategoryVO vo = new ActressCategoryVO();
        vo.setActress(actress);
        vo.setCategories(categories);
        return vo;
    }

}
