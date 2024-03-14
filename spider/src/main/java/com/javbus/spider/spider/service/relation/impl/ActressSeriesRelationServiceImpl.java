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
import com.javbus.spider.spider.entity.vo.ActressSeriesVo;
import com.javbus.spider.spider.service.relation.ActressSeriesRelationService;

@Service
public class ActressSeriesRelationServiceImpl implements ActressSeriesRelationService {
    @Autowired
    private ActressSeriesDao ActressSeriesDao;
    @Autowired
    private SeriesDao seriesDao;
    @Autowired
    private ActressDao ActressDao;

    @Override
    public void saveRelation(ActressSeriesVo vo) {
        // TODO Auto-generated method stub
        List<Actress> actresses = vo.getActress();
        List<String> names = actresses.stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> ActressIds = ActressDao.queryActressIdsByNames(names);
        if (ActressIds == null || ActressIds.isEmpty()) {
            ActressDao.saveActresses(actresses);
            ActressIds = ActressDao.queryActressIdsByNames(names);
        }
        Series series = seriesDao.querySeriesByName(vo.getSeries().getName());
        if (series == null) {
            seriesDao.save(vo.getSeries());
            series = seriesDao.querySeriesByName(vo.getSeries().getName());
        }
        List<ActressSeriesRelation> ActressSeriesRelations = ActressSeriesDao.queryActressSeriesRelations(ActressIds, series.getId());
        if (ActressSeriesRelations == null || ActressSeriesRelations.isEmpty()) {
            final Series final_series = series;
            List<ActressSeriesRelation> relations = ActressIds.stream().map((id) -> {
                ActressSeriesRelation relation = new ActressSeriesRelation();
                relation.setSeriesId(final_series.getId());
                relation.setActressId(id);
                return relation;
            }).collect(Collectors.toList());
            ActressSeriesDao.addActressSeriesRelations(relations);
        }

    }

}
