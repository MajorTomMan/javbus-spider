package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.SeriesDao;
import com.javbus.spider.spider.dao.base.StarDao;
import com.javbus.spider.spider.dao.relation.StarSeriesDao;
import com.javbus.spider.spider.entity.base.Series;
import com.javbus.spider.spider.entity.base.Star;
import com.javbus.spider.spider.entity.relation.StarSeriesRelation;
import com.javbus.spider.spider.entity.vo.StarSeriesVo;
import com.javbus.spider.spider.service.relation.StarSeriesRelationService;

@Service
public class StarSeriesRelationServiceImpl implements StarSeriesRelationService {
    @Autowired
    private StarSeriesDao starSeriesDao;
    @Autowired
    private SeriesDao seriesDao;
    @Autowired
    private StarDao starDao;

    @Override
    public void saveRelation(StarSeriesVo vo) {
        // TODO Auto-generated method stub
        List<Star> stars = vo.getStars();
        List<String> names = stars.stream().map((star) -> {
            return star.getName();
        }).collect(Collectors.toList());
        List<Integer> starIds = starDao.queryStarIdsByNames(names);
        if (starIds == null || starIds.isEmpty()) {
            starDao.saveStars(stars);
            starIds = starDao.queryStarIdsByNames(names);
        }
        Series series = seriesDao.querySeriesByName(vo.getSeries().getName());
        if (series == null) {
            seriesDao.save(vo.getSeries());
            series = seriesDao.querySeriesByName(vo.getSeries().getName());
        }
        List<StarSeriesRelation> starSeriesRelations = starSeriesDao.queryStarSeriesRelations(starIds, series.getId());
        if (starSeriesRelations == null || starSeriesRelations.isEmpty()) {
            final Series final_series = series;
            List<StarSeriesRelation> relations = starIds.stream().map((id) -> {
                StarSeriesRelation relation = new StarSeriesRelation();
                relation.setSeriesId(final_series.getId());
                relation.setStarId(id);
                return relation;
            }).collect(Collectors.toList());
            starSeriesDao.addStarSeriesRelations(relations);
        }

    }

}
