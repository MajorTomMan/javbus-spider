package com.javbus.spider.spider.service.relation.impl;

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
            movieDao.saveMovie(dto.getMovie());
        } else {
            movieDao.updateMovie(dto.getMovie());
        }
        movie = movieDao.queryMovieByCode(dto.getMovie().getCode());
        // -----------------Magnet------------------------------
        List<Magnet> magnets = magnetDao
                .queryMagnets(dto.getMagnets().stream().map(magnet -> magnet.getLink()).toList());
        if (magnets.isEmpty()) {
            magnetDao.saveMagnets(magnets);
        } else if (magnets.size() < dto.getMagnets().size()) {
            List<Magnet> finalMagnets = magnets;
            List<Magnet> newMagnetList = dto.getMagnets().stream()
                    .filter(magnet -> {
                        return finalMagnets.stream().noneMatch(m -> m.getLink().equals(magnet.getLink()));
                    }).toList();
            magnetDao.saveMagnets(newMagnetList);
        } else {
            magnetDao.updateMagnets(dto.getMagnets());
        }
        // ----------------------Relations------------------------------
        List<MovieMagnetRelation> movieMagnetRelations = movieMagnetDao.queryRelationsByMovieId(movie.getId());
        Movie finalMovie = movie;
        List<MovieMagnetRelation> relations = dto.getMagnets().stream().map(magnet -> {
            MovieMagnetRelation r = new MovieMagnetRelation();
            r.setMovieId(finalMovie.getId());
            r.setMagnetId(magnet.getId());
            return r;
        }).collect(Collectors.toList());
        if (movieMagnetRelations.isEmpty()) {
            movieMagnetDao.addMovieMagnetRelations(relations);
        } else if (movieMagnetRelations.size() < relations.size()) {
            List<MovieMagnetRelation> newRelation = relations.stream().filter(relation -> {
                return movieMagnetRelations.stream().noneMatch(r -> {
                    return relation.getMagnetId() == r.getMagnetId() && relation.getMovieId() == r.getMovieId();
                });
            }).toList();
            movieMagnetDao.addMovieMagnetRelations(newRelation);
        } else {
            movieMagnetDao.updateMovieMagnetRelations(relations);
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
