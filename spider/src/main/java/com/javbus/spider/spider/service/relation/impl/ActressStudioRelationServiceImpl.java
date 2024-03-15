package com.javbus.spider.spider.service.relation.impl;

import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.dao.base.StudioDao;
import com.javbus.spider.spider.dao.relation.ActressStudioDao;
import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.base.Studio;
import com.javbus.spider.spider.entity.relation.ActressStudioRelation;
import com.javbus.spider.spider.entity.vo.ActressStudioVO;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.entity.dto.ActressStudioDTO;
import com.javbus.spider.spider.service.relation.ActressStudioRelationService;

@Service
public class ActressStudioRelationServiceImpl implements ActressStudioRelationService {
    @Autowired
    private ActressStudioDao actressStudioDao;
    @Autowired
    private StudioDao studioDao;
    @Autowired
    private ActressDao actressDao;

    @Override
    public void saveRelation(ActressStudioDTO dto) {
        // TODO Auto-generated method stub
        List<Actress> actresses = dto.getActress();
        List<String> names = actresses.stream().map(Actress -> Actress.getName()).collect(Collectors.toList());
        List<Integer> ActressIds = actressDao.queryActressIdsByNames(names);
        if (ActressIds == null || ActressIds.isEmpty()) {
            actressDao.saveActresses(actresses);
            ActressIds = actressDao.queryActressIdsByNames(names);
        }
        Studio studio = studioDao.queryStudioByName(dto.getStudio().getName());
        if (studio == null) {
            studioDao.save(dto.getStudio());
            studio = studioDao.queryStudioByName(dto.getStudio().getName());
        }
        List<ActressStudioRelation> ActressStudioRelations = actressStudioDao.queryActressStudioRelations(ActressIds,
                studio.getId());
        if (ActressStudioRelations == null || ActressStudioRelations.isEmpty()) {
            final Studio final_studio = studio;
            List<ActressStudioRelation> relations = ActressIds.stream().map((id) -> {
                ActressStudioRelation relation = new ActressStudioRelation();
                relation.setActressId(id);
                relation.setStudioId(final_studio.getId());
                return relation;
            }).collect(Collectors.toList());
            actressStudioDao.addActressStudioRelations(relations);
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
