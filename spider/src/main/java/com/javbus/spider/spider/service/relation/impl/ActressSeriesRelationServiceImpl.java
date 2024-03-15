package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.SeriesDao;
import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.dao.relation.ActressSeriesDao;
import com.javbus.spider.spider.entity.base.Series;
import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.relation.ActressSeriesRelation;
import com.javbus.spider.spider.entity.vo.ActressSeriesVO;
import com.javbus.spider.spider.entity.dto.ActressSeriesDTO;
import com.javbus.spider.spider.service.relation.ActressSeriesRelationService;

@Service
public class ActressSeriesRelationServiceImpl implements ActressSeriesRelationService {
    @Autowired
    private ActressSeriesDao actressSeriesDao;
    @Autowired
    private SeriesDao seriesDao;
    @Autowired
    private ActressDao actressDao;

    @Override
    public void saveRelation(ActressSeriesDTO dto) {
        // TODO Auto-generated method stub
        List<Actress> actresses = dto.getActress();
        List<String> names = actresses.stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> ActressIds = actressDao.queryActressIdsByNames(names);
        if (ActressIds == null || ActressIds.isEmpty()) {
            actressDao.saveActresses(actresses);
            ActressIds = actressDao.queryActressIdsByNames(names);
        }
        Series series = seriesDao.querySeriesByName(dto.getSeries().getName());
        if (series == null) {
            seriesDao.save(dto.getSeries());
            series = seriesDao.querySeriesByName(dto.getSeries().getName());
        }
        List<ActressSeriesRelation> ActressSeriesRelations = actressSeriesDao.queryActressSeriesRelations(ActressIds,
                series.getId());
        if (ActressSeriesRelations == null || ActressSeriesRelations.isEmpty()) {
            final Series final_series = series;
            List<ActressSeriesRelation> relations = ActressIds.stream().map((id) -> {
                ActressSeriesRelation relation = new ActressSeriesRelation();
                relation.setSeriesId(final_series.getId());
                relation.setActressId(id);
                return relation;
            }).collect(Collectors.toList());
            actressSeriesDao.addActressSeriesRelations(relations);
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
