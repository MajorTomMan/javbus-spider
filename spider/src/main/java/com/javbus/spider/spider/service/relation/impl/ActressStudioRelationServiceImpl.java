package com.javbus.spider.spider.service.relation.impl;

import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.dao.base.StudioDao;
import com.javbus.spider.spider.dao.relation.ActressStudioDao;
import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.base.Studio;
import com.javbus.spider.spider.entity.relation.ActressStudioRelation;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.entity.vo.ActressStudioVo;
import com.javbus.spider.spider.service.relation.ActressStudioRelationService;

@Service
public class ActressStudioRelationServiceImpl implements ActressStudioRelationService {
    @Autowired
    private ActressStudioDao ActressStudioDao;
    @Autowired
    private StudioDao studioDao;
    @Autowired
    private ActressDao ActressDao;

    @Override
    public void saveRelation(ActressStudioVo vo) {
        // TODO Auto-generated method stub
        List<Actress> actresses = vo.getActress();
        List<String> names = actresses.stream().map(Actress -> Actress.getName()).collect(Collectors.toList());
        List<Integer> ActressIds = ActressDao.queryActressIdsByNames(names);
        if (ActressIds == null || ActressIds.isEmpty()) {
            ActressDao.saveActresses(actresses);
            ActressIds = ActressDao.queryActressIdsByNames(names);
        }
        Studio studio = studioDao.queryStudioByName(vo.getStudio().getName());
        if (studio == null) {
            studioDao.save(vo.getStudio());
            studio = studioDao.queryStudioByName(vo.getStudio().getName());
        }
        List<ActressStudioRelation> ActressStudioRelations = ActressStudioDao.queryActressStudioRelations(ActressIds, studio.getId());
        if (ActressStudioRelations == null || ActressStudioRelations.isEmpty()) {
            final Studio final_studio = studio;
            List<ActressStudioRelation> relations = ActressIds.stream().map((id) -> {
                ActressStudioRelation relation = new ActressStudioRelation();
                relation.setActressId(id);
                relation.setStudioId(final_studio.getId());
                return relation;
            }).collect(Collectors.toList());
            ActressStudioDao.addActressStudioRelations(relations);
        }
        
    }

}
