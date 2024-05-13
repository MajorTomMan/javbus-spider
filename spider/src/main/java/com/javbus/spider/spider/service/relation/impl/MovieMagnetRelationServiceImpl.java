package com.javbus.spider.spider.service.relation.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MagnetDao;
import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.relation.MovieMagnetDao;
import com.javbus.spider.spider.entity.base.Magnet;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.dto.MovieMagnetDTO;
import com.javbus.spider.spider.entity.relation.MovieMagnetRelation;
import com.javbus.spider.spider.service.relation.MovieMagnetRelationService;

@Service
public class MovieMagnetRelationServiceImpl implements MovieMagnetRelationService {
    @Autowired
    private MovieDao movieDao;
    @Autowired
    private MagnetDao magnetDao;
    @Autowired
    private MovieMagnetDao movieMagnetDao;

    @Override
    public void saveRelation(MovieMagnetDTO dto) {
        // TODO Auto-generated method stub
        // 保存或更新电影信息
        Movie movie = movieDao.queryMovieByCode(dto.getMovie().getCode());
        if (movie == null) {
            movieDao.saveMovie(movie);
        } else {
            movieDao.updateMovie(movie);
        }

        List<Magnet> newMagnets = new ArrayList<>();
        for (Magnet magnet : dto.getMagnets()) {
            if (magnetDao.queryMagnetByLink(magnet.getLink()) == null) {
                newMagnets.add(magnet);
            } else {
                magnetDao.updateMagnet(magnet);
            }
        }
        magnetDao.saveMagnets(newMagnets);
        List<String> links = dto.getMagnets().stream().map(m -> m.getLink()).collect(Collectors.toList());
        // 获取保存后的磁力链接列表
        List<Magnet> savedMagnets = magnetDao.queryMagnets(links);
        // 保存电影与磁力链接关系
        List<MovieMagnetRelation> relation = movieMagnetDao.queryRelationsByMovieId(movie.getId());
        if (relation == null || relation.isEmpty()) {
            List<MovieMagnetRelation> relations = savedMagnets.stream().map(m -> {
                MovieMagnetRelation r = new MovieMagnetRelation();
                r.setMovieId(movie.getId());
                r.setMagnetId(m.getId());
                return r;
            }).collect(Collectors.toList());
            movieMagnetDao.saveRelations(relations);
        } else {
            movieMagnetDao.updateRelations(relation);
        }
    }

    @Override
    public List<MovieMagnetRelation> queryRelationsByMovieId(Integer movieId) {
        // TODO Auto-generated method stub
        return movieMagnetDao.queryRelationsByMovieId(movieId);
    }

    @Override
    public List<MovieMagnetRelation> queryRelationsByMagnetId(Integer magnetId) {
        // TODO Auto-generated method stub
        return movieMagnetDao.queryRelationsByMagnetId(magnetId);

    }
}
