package com.jav.server.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.jav.server.dao.base.SeriesDao;
import com.jav.server.dao.base.ActressDao;
import com.jav.server.dao.relation.ActressSeriesDao;
import com.jav.server.entity.base.Series;
import com.jav.server.entity.base.Actress;
import com.jav.server.entity.relation.ActressSeriesRelation;
import com.jav.server.entity.vo.ActressSeriesVO;
import com.jav.server.entity.dto.ActressSeriesDTO;
import com.jav.server.service.relation.ActressSeriesRelationService;

@Service
public class ActressSeriesRelationServiceImpl implements ActressSeriesRelationService {
    @Autowired
    private ActressSeriesDao actressSeriesDao;
    @Autowired
    private SeriesDao seriesDao;
    @Autowired
    private ActressDao actressDao;

    @Override
    @Transactional
    public void saveRelation(ActressSeriesDTO dto) {
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
        // ------------------------Series------------------------------------
        Series series = seriesDao.querySeriesByName(dto.getSeries().getName());
        if (series == null) {
            seriesDao.save(dto.getSeries());
            series = seriesDao.querySeriesByName(dto.getSeries().getName());
        } else {
            seriesDao.updateSeries(dto.getSeries());
        }
        // --------------------------Relation------------------------------
        List<ActressSeriesRelation> actressSeriesRelations = actressSeriesDao.queryActressSeriesRelations(actressIds,
                series.getId());
        final Series final_series = series;
        List<ActressSeriesRelation> relations = actressIds.stream().map((id) -> {
            ActressSeriesRelation relation = new ActressSeriesRelation();
            relation.setSeriesId(final_series.getId());
            relation.setActressId(id);
            return relation;
        }).collect(Collectors.toList());
        if (actressSeriesRelations.isEmpty()) {
            actressSeriesDao.addActressSeriesRelations(relations);
        } else if (actressSeriesRelations.size() < relations.size()) {
            // 处理新增的关系
            List<ActressSeriesRelation> newRelation = relations.stream().filter(relation -> {
                return actressSeriesRelations.stream().noneMatch(r -> {
                    return relation.getActressId() == r.getActressId() && relation.getSeriesId() == r.getSeriesId();
                });
            }).toList();
            actressSeriesDao.addActressSeriesRelations(newRelation);
        } else {
            actressSeriesDao.updateActressSeriesRelations(relations);
        }

    }

    @Override
    public ActressSeriesVO queryRelations(Integer actressId) {
        // TODO Auto-generated method stub
        List<ActressSeriesRelation> relations = actressSeriesDao.queryActressSeriesRelationsByActressId(actressId);
        if (relations == null || relations.isEmpty()) {
            return null;
        }
        Actress actress = actressDao.queryActressById(actressId);
        List<Integer> seriesIds = relations.stream().map(re -> {
            return re.getSeriesId();
        }).collect(Collectors.toList());
        List<Series> series = seriesDao.querySeriesByIds(seriesIds);
        ActressSeriesVO vo = new ActressSeriesVO();
        vo.setActress(actress);
        vo.setSeries(series);
        return vo;
    }

}
