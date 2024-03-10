package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.StarDao;
import com.javbus.spider.spider.dao.relation.StarCensorDao;
import com.javbus.spider.spider.entity.base.Star;
import com.javbus.spider.spider.entity.relation.StarCensorRelation;
import com.javbus.spider.spider.entity.vo.StarCensorVo;
import com.javbus.spider.spider.service.relation.StarCensorRelationService;

@Service
public class StarCensorRelationServiceImpl implements StarCensorRelationService {
    @Autowired
    private StarCensorDao starCensorDao;
    @Autowired
    private StarDao starDao;

    @Override
    public void saveRelation(StarCensorVo vo) {
        // TODO Auto-generated method stub
        List<Star> stars = vo.getStars();
        starDao.saveStars(stars);
        List<String> names = stars.stream().map(star -> star.getName()).collect(Collectors.toList());
        List<Integer> ids = starDao.queryStarIdsByNames(names);
        List<StarCensorRelation> relations = ids.stream().map(id -> {
            StarCensorRelation relation = new StarCensorRelation();
            relation.setIsCensored(vo.getIsCensored());
            relation.setStarId(id);
            return relation;
        }).collect(Collectors.toList());
        starCensorDao.addStarCensorRelations(relations);
    }

}
