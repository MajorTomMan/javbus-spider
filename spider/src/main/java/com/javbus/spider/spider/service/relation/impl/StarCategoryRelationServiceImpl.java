package com.javbus.spider.spider.service.relation.impl;

import com.javbus.spider.spider.dao.base.CategoryDao;
import com.javbus.spider.spider.dao.base.StarDao;
import com.javbus.spider.spider.dao.relation.StarCategoryDao;
import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Star;
import com.javbus.spider.spider.entity.relation.StarCategoryRelation;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.entity.vo.StarCategoryVo;
import com.javbus.spider.spider.service.relation.StarCategoryRelationService;

@Service
public class StarCategoryRelationServiceImpl implements StarCategoryRelationService {
    @Autowired
    private StarCategoryDao starCategoryDao;
    @Autowired
    private CategoryDao categoryDao;
    @Autowired
    private StarDao starDao;

    @Override
    public void saveRelation(StarCategoryVo vo) {
        // TODO Auto-generated method stub
        List<Star> stars = vo.getStars();
        List<String> starNames = stars.stream().map((star) -> {
            return star.getName();
        }).collect(Collectors.toList());
        List<Integer> starIds = starDao.queryStarIdsByNames(starNames);
        if(starIds==null||starIds.isEmpty()){
            starDao.saveStars(stars);
            starIds = starDao.queryStarIdsByNames(starNames);
        }
        List<Category> categories = vo.getCategories();
        // 先保存进数据库保证数据存在
        categoryDao.saveCategories(categories);
        List<String> categoryNames = categories.stream().map((category) -> {
            return category.getName();
        }).collect(Collectors.toList());
        List<Integer> categoryIds = categoryDao.queryCategoryIdsByNames(categoryNames);
        if(categoryIds==null||categoryIds.isEmpty()){
            categoryDao.saveCategories(categories);
            categoryIds = categoryDao.queryCategoryIdsByNames(categoryNames);
        }
        List<StarCategoryRelation> relations = new ArrayList<>();
        // 处理多对多关系
        for (Integer starId : starIds) {
            for (Integer categoryId : categoryIds) {
                StarCategoryRelation relation = new StarCategoryRelation();
                relation.setCategoryId(categoryId);
                relation.setStarId(starId);
                relations.add(relation);
            }
        }
        starCategoryDao.addStarCategoryRelations(relations);
    }

}
