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
        List<String> names = dto.getActress().stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> actressIds = actressDao.queryActressIdsByNames(names);
        if (actressIds.isEmpty() || actressIds.size() != dto.getActress().size()) {
            actressDao.saveActresses(dto.getActress());
            actressIds = actressDao.queryActressIdsByNames(names);
        } else {
            for (int i = 0; i < actressIds.size(); i++) {
                dto.getActress().get(i).setId(actressIds.get(i));
            }
            actressDao.updateActresses(dto.getActress());
        }
        Series series = seriesDao.querySeriesByName(dto.getSeries().getName());
        if (series == null) {
            seriesDao.save(dto.getSeries());
            series = seriesDao.querySeriesByName(dto.getSeries().getName());
        } else {
            seriesDao.updateSeries(dto.getSeries());
        }
        List<ActressSeriesRelation> actressSeriesRelations = actressSeriesDao.queryActressSeriesRelations(actressIds,
                series.getId());
        if (actressSeriesRelations.isEmpty()) {
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
