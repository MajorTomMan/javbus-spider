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
        actressDao.saveActresses(dto.getActress());
        List<String> names = dto.getActress().stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> actressIds = actressDao.queryActressIdsByNames(names);
        seriesDao.save(dto.getSeries());
        Series series = seriesDao.querySeriesByName(dto.getSeries().getName());
        List<ActressSeriesRelation> ActressSeriesRelations = actressSeriesDao.queryActressSeriesRelations(actressIds,
                series.getId());
        if (ActressSeriesRelations == null || ActressSeriesRelations.isEmpty()) {
            final Series final_series = series;
            List<ActressSeriesRelation> relations = actressIds.stream().map((id) -> {
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
