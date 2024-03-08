package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.DirectorDao;
import com.javbus.spider.spider.dao.base.StarDao;
import com.javbus.spider.spider.dao.relation.StarDirectorDao;
import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.relation.StarDirectorRelation;
import com.javbus.spider.spider.entity.vo.StarDirectorVo;
import com.javbus.spider.spider.service.relation.StarDirectorRelationService;

@Service
public class StarDirectorRelationServiceImpl implements StarDirectorRelationService {
    @Autowired
    private StarDirectorDao starDirectorDao;
    @Autowired
    private DirectorDao directorDao;
    @Autowired
    private StarDao starDao;

    @Override
    public void saveRelation(StarDirectorVo vo) {
        // TODO Auto-generated method stub
        if (vo == null) {
            return;
        }
        Director director = directorDao.queryDirectorByName(vo.getDirector().getName());
        if (director == null) {
            directorDao.save(vo.getDirector());
            director = directorDao.queryDirectorByName(vo.getDirector().getName());
        }
        List<String> names = vo.getStars().stream().map((star) -> {
            return star.getName();
        }).collect(Collectors.toList());
        List<Integer> ids = starDao.queryStarIdsByNames(names);
        if (ids == null || ids.isEmpty()) {
            starDao.saveStars(vo.getStars());
            ids = starDao.queryStarIdsByNames(names);
        }
        final Director final_Director=director;
        List<StarDirectorRelation> relations = ids.stream().map((id) -> {
            StarDirectorRelation relation = new StarDirectorRelation();
            relation.setDirectorId(final_Director.getId());
            relation.setStarId(id);
            return relation;
        }).collect(Collectors.toList());
        starDirectorDao.addStarDirectorRelations(relations);
    }

}
