package com.jav.server.service.relation.impl;

import com.jav.server.dao.base.ActressDao;
import com.jav.server.dao.base.StudioDao;
import com.jav.server.dao.relation.ActressStudioDao;
import com.jav.server.entity.base.Actress;
import com.jav.server.entity.base.Studio;
import com.jav.server.entity.relation.ActressStudioRelation;
import com.jav.server.entity.vo.ActressStudioVO;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.jav.server.entity.dto.ActressStudioDTO;
import com.jav.server.service.relation.ActressStudioRelationService;

@Service
public class ActressStudioRelationServiceImpl implements ActressStudioRelationService {
    @Autowired
    private ActressStudioDao actressStudioDao;
    @Autowired
    private StudioDao studioDao;
    @Autowired
    private ActressDao actressDao;

    @Override
    @Transactional
    public void saveRelation(ActressStudioDTO dto) {
        // TODO Auto-generated method stub
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
        // -----------------------------Studio----------------------------------
        Studio studio = studioDao.queryStudioByName(dto.getStudio().getName());
        if (studio == null) {
            studioDao.save(dto.getStudio());
        } else {
            studioDao.update(dto.getStudio());
        }
        studio = studioDao.queryStudioByName(dto.getStudio().getName());
        // ---------------------------Relation----------------------------
        List<ActressStudioRelation> actressStudioRelations = actressStudioDao.queryActressStudioRelations(actressIds,
                studio.getId());
        final Studio final_studio = studio;
        List<ActressStudioRelation> relations = actressIds.stream().map((id) -> {
            ActressStudioRelation relation = new ActressStudioRelation();
            relation.setActressId(id);
            relation.setStudioId(final_studio.getId());
            return relation;
        }).collect(Collectors.toList());
        if (actressStudioRelations.isEmpty()) {
            actressStudioDao.addActressStudioRelations(relations);
        } else if (actressStudioRelations.size() < relations.size()) {
            // 处理新增的关系
            List<ActressStudioRelation> newRelation = relations.stream().filter(relation -> {
                return actressStudioRelations.stream().noneMatch(r -> {
                    return relation.getActressId() == r.getActressId() && relation.getStudioId() == r.getStudioId();
                });
            }).toList();
            actressStudioDao.addActressStudioRelations(newRelation);
        } else {
            actressStudioDao.updateActressStudioRelations(relations);
        }

    }

    @Override
    public ActressStudioVO queryRelations(Integer actressId) {
        // TODO Auto-generated method stub
        List<ActressStudioRelation> relations = actressStudioDao.queryActressStudioRelationByActressId(actressId);
        if (relations == null || relations.isEmpty()) {
            return null;
        }
        Actress actress = actressDao.queryActressById(actressId);
        List<Integer> studioIds = relations.stream().map(relation -> {
            return relation.getStudioId();
        }).collect(Collectors.toList());
        List<Studio> studios = studioDao.queryStudioByIds(studioIds);
        ActressStudioVO vo = new ActressStudioVO();
        vo.setActress(actress);
        vo.setStudios(studios);
        return vo;
    }

}
