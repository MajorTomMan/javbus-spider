package com.jav.server.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.jav.server.dao.base.DirectorDao;
import com.jav.server.dao.base.ActressDao;
import com.jav.server.dao.relation.ActressDirectorDao;
import com.jav.server.entity.base.Actress;
import com.jav.server.entity.base.Director;
import com.jav.server.entity.relation.ActressDirectorRelation;
import com.jav.server.entity.vo.ActressDirectorVO;
import com.jav.server.entity.dto.ActressDirectorDTO;
import com.jav.server.service.relation.ActressDirectorRelationService;

@Service
public class ActressDirectorRelationServiceImpl implements ActressDirectorRelationService {
    @Autowired
    private ActressDirectorDao actressDirectorDao;
    @Autowired
    private DirectorDao directorDao;
    @Autowired
    private ActressDao actressDao;

    @Override
    @Transactional
    public void saveRelation(ActressDirectorDTO dto) {
        // TODO Auto-generated method stub
        Director director = directorDao.queryDirectorByName(dto.getDirector().getName());
        if (director == null) {
            directorDao.save(dto.getDirector());
            director = directorDao.queryDirectorByName(dto.getDirector().getName());
        } else {
            directorDao.update(dto.getDirector());
        }
        // -------------------------Actresses--------------------------
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
        // --------------------------Relation------------------------------
        List<ActressDirectorRelation> actressDirectorRelations = actressDirectorDao
                .queryActressDirectorRelations(actressIds, director.getId());
        final Director final_Director = director;
        List<ActressDirectorRelation> relations = actressIds.stream().map((id) -> {
            ActressDirectorRelation relation = new ActressDirectorRelation();
            relation.setDirectorId(final_Director.getId());
            relation.setActressId(id);
            return relation;
        }).collect(Collectors.toList());
        if (actressDirectorRelations.isEmpty()) {
            actressDirectorDao.addActressDirectorRelations(relations);
        }
        if (actressDirectorRelations.size() < relations.size()) {
            List<ActressDirectorRelation> newRelation = relations.stream().filter(relation -> {
                return actressDirectorRelations.stream().noneMatch(r -> {
                    return relation.getActressId() == r.getActressId() && relation.getDirectorId() == r.getDirectorId();
                });
            }).toList();
            actressDirectorDao.addActressDirectorRelations(newRelation);
        } else {
            actressDirectorDao.updateActressDirectorRelations(relations);
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
