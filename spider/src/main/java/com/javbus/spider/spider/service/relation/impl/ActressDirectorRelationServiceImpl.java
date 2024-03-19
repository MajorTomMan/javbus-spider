package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.DirectorDao;
import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.dao.relation.ActressDirectorDao;
import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.relation.ActressDirectorRelation;
import com.javbus.spider.spider.entity.vo.ActressDirectorVO;
import com.javbus.spider.spider.entity.dto.ActressDirectorDTO;
import com.javbus.spider.spider.service.relation.ActressDirectorRelationService;

@Service
public class ActressDirectorRelationServiceImpl implements ActressDirectorRelationService {
    @Autowired
    private ActressDirectorDao actressDirectorDao;
    @Autowired
    private DirectorDao directorDao;
    @Autowired
    private ActressDao actressDao;

    @Override
    public void saveRelation(ActressDirectorDTO dto) {
        // TODO Auto-generated method stub
        Director director = directorDao.queryDirectorByName(dto.getDirector().getName());
        if (director == null) {
            directorDao.save(dto.getDirector());
            director = directorDao.queryDirectorByName(dto.getDirector().getName());
        } else {
            directorDao.update(dto.getDirector());
        }
        List<String> names = dto.getActress().stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> actressIds = actressDao.queryActressIdsByNames(names);
        if (actressIds.isEmpty()) {
            actressDao.saveActresses(dto.getActress());
            actressIds = actressDao.queryActressIdsByNames(names);
        } else {
            for (int i = 0; i <= actressIds.size(); i++) {
                dto.getActress().get(i).setId(actressIds.get(i));
            }
            actressDao.updateActresses(dto.getActress());
        }
        List<ActressDirectorRelation> actressDirectorRelations = actressDirectorDao
                .queryActressDirectorRelations(actressIds, director.getId());
        if (actressDirectorRelations.isEmpty()) {
            final Director final_Director = director;
            List<ActressDirectorRelation> relations = actressIds.stream().map((id) -> {
                ActressDirectorRelation relation = new ActressDirectorRelation();
                relation.setDirectorId(final_Director.getId());
                relation.setActressId(id);
                return relation;
            }).collect(Collectors.toList());
            actressDirectorDao.addActressDirectorRelations(relations);
        }

    }

    @Override
    public ActressDirectorVO queryRelations(Integer actressId) {
        // TODO Auto-generated method stub
        ActressDirectorRelation relation = actressDirectorDao.queryActressDirectorRelationByActressId(actressId);
        if (relation == null) {
            return null;
        }
        Actress actress = actressDao.queryActressById(actressId);
        Director director = directorDao.queryDirectorById(relation.getDirectorId());
        ActressDirectorVO vo = new ActressDirectorVO();
        vo.setActress(actress);
        vo.setDirector(director);
        return vo;
    }

}
