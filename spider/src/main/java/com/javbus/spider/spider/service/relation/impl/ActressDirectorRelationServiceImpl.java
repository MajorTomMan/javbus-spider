package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.DirectorDao;
import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.dao.relation.ActressDirectorDao;
import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.relation.ActressDirectorRelation;
import com.javbus.spider.spider.entity.vo.ActressDirectorVo;
import com.javbus.spider.spider.service.relation.ActressDirectorRelationService;

@Service
public class ActressDirectorRelationServiceImpl implements ActressDirectorRelationService {
    @Autowired
    private ActressDirectorDao ActressDirectorDao;
    @Autowired
    private DirectorDao directorDao;
    @Autowired
    private ActressDao ActressDao;

    @Override
    public void saveRelation(ActressDirectorVo vo) {
        // TODO Auto-generated method stub
        Director director = directorDao.queryDirectorByName(vo.getDirector().getName());
        if (director == null) {
            directorDao.save(vo.getDirector());
            director = directorDao.queryDirectorByName(vo.getDirector().getName());
        }
        List<String> names = vo.getActress().stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> ActressIds = ActressDao.queryActressIdsByNames(names);
        if (ActressIds == null || ActressIds.isEmpty()) {
            ActressDao.saveActresses(vo.getActress());
            ActressIds = ActressDao.queryActressIdsByNames(names);
        }
        List<ActressDirectorRelation> ActressDirectorRelations = ActressDirectorDao.queryActressDirectorRelations(ActressIds, director.getId());
        if(ActressDirectorRelations==null|| ActressDirectorRelations.isEmpty()){
            final Director final_Director = director;
            List<ActressDirectorRelation> relations = ActressIds.stream().map((id) -> {
                ActressDirectorRelation relation = new ActressDirectorRelation();
                relation.setDirectorId(final_Director.getId());
                relation.setActressId(id);
                return relation;
            }).collect(Collectors.toList());
            ActressDirectorDao.addActressDirectorRelations(relations);
        }

    }

}
