package com.javbus.spider.spider.service.relation.impl;

import com.javbus.spider.spider.dao.base.StarDao;
import com.javbus.spider.spider.dao.base.StudioDao;
import com.javbus.spider.spider.dao.relation.StarStudioDao;
import com.javbus.spider.spider.entity.base.Star;
import com.javbus.spider.spider.entity.base.Studio;
import com.javbus.spider.spider.entity.relation.StarStudioRelation;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.entity.vo.StarStudioVo;
import com.javbus.spider.spider.service.relation.StarStudioRelationService;

@Service
public class StarStudioRelationServiceImpl implements StarStudioRelationService {
    @Autowired
    private StarStudioDao starStudioDao;
    @Autowired
    private StudioDao studioDao;
    @Autowired
    private StarDao starDao;

    @Override
    public void saveRelation(StarStudioVo vo) {
        // TODO Auto-generated method stub
        if (vo == null) {
            return;
        }
        List<Star> stars = vo.getStars();
        List<String> names = stars.stream().map(star -> star.getName()).collect(Collectors.toList());
        List<Integer> ids = starDao.queryStarIdsByNames(names);
        if (ids == null || ids.isEmpty()) {
            starDao.saveStars(stars);
            ids = starDao.queryStarIdsByNames(names);
        }
        Studio studio = studioDao.queryStudioByName(vo.getStudio().getName());
        if(studio==null){
            studioDao.save(vo.getStudio());
            studio = studioDao.queryStudioByName(vo.getStudio().getName());
        }
        final Studio final_studio = studio;
        List<StarStudioRelation> relations=ids.stream().map((id)->{
           StarStudioRelation relation = new StarStudioRelation();
           relation.setStarId(id);
           relation.setStudioId(final_studio.getId());
           return relation;
        }).collect(Collectors.toList());
        starStudioDao.addStarStudioRelations(relations);
    }

}
