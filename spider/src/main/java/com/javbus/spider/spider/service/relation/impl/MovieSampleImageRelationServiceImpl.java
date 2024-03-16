package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.SampleImageDao;
import com.javbus.spider.spider.dao.dto.MovieActressSampleImageDao;
import com.javbus.spider.spider.dao.relation.MovieSampleImageDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.SampleImage;
import com.javbus.spider.spider.entity.dto.ImageDTO;
import com.javbus.spider.spider.entity.dto.SampleImageDTO;
import com.javbus.spider.spider.entity.relation.MovieSampleImageRelation;
import com.javbus.spider.spider.entity.vo.MovieSampleImageVO;
import com.javbus.spider.spider.entity.dto.MovieSampleImageDTO;
import com.javbus.spider.spider.service.relation.MovieSampleImageRelationService;
import com.javbus.spider.spider.utils.ImageUtil;

@Service
public class MovieSampleImageRelationServiceImpl implements MovieSampleImageRelationService {
    @Autowired
    private MovieActressSampleImageDao movieActressSampleImageDao;
    @Autowired
    private MovieSampleImageDao movieSampleImageDao;
    @Autowired
    private SampleImageDao sampleImageDao;
    @Autowired
    private MovieDao movieDao;
    @Autowired
    private ImageUtil imageUtil;

    @Override
    public void saveRelation(MovieSampleImageDTO dto) {
        // TODO Auto-generated method stub
        movieDao.saveMovie(dto.getMovie());
        Movie movie = movieDao.queryMovieByCode(dto.getMovie().getCode());
        sampleImageDao.saveSampleImages(dto.getSampleImages());
        List<Integer> sampleImageIds = sampleImageDao.querySampleImageIdsByLinks(dto.getSampleImages());
        List<MovieSampleImageRelation> movieSampleImageRelations = movieSampleImageDao
                .queryMovieSampleImageRelations(movie.getId(), sampleImageIds);
        if (movieSampleImageRelations == null || movieSampleImageRelations.isEmpty()) {
            final Movie final_movie = movie;
            List<MovieSampleImageRelation> relations = sampleImageIds.stream().map((id) -> {
                MovieSampleImageRelation relation = new MovieSampleImageRelation();
                relation.setMovieId(final_movie.getId());
                relation.setSampleImageId(id);
                return relation;
            }).collect(Collectors.toList());
            movieSampleImageDao.addMovieSampleImageRelations(relations);
            List<ImageDTO> imageDTOs = movieActressSampleImageDao.queryImageDao(movie.getId());
            if (imageDTOs == null || imageDTOs.isEmpty()) {
                return;
            }
            List<SampleImageDTO> sampleImageDTOs = imageDTOs.stream().map(imageDTO -> {
                SampleImageDTO sampleImageDTO = new SampleImageDTO();
                sampleImageDTO.setCode(imageDTO.getCode());
                sampleImageDTO.setName(imageDTO.getName());
                String[] split = imageDTO.getLink().split("/");
                String fileName = split[split.length - 1];
                sampleImageDTO.setFileName(fileName);
                if (!imageUtil.checkImageIsExists(sampleImageDTO)) {
                    byte[] data = imageUtil.download(imageDTO.getLink());
                    sampleImageDTO.setSampleImage(data);
                } else {
                    sampleImageDTO.setSampleImage(null);
                }
                return sampleImageDTO;
            }).filter(imageDTO -> imageDTO.getSampleImage() != null).collect(Collectors.toList());
            imageUtil.saveSampleImage(sampleImageDTOs);
        }
    }

    @Override
    public MovieSampleImageVO queryRelations(Integer movieId) {
        // TODO Auto-generated method stub
        List<MovieSampleImageRelation> relations = movieSampleImageDao.queryMovieSampleImageRelationsByMovieId(movieId);
        if (relations == null || relations.isEmpty()) {
            return null;
        }
        Movie movie = movieDao.queryMovieById(movieId);
        List<Integer> sampleImageIds = relations.stream().map(relation -> {
            return relation.getSampleImageId();
        }).collect(Collectors.toList());
        List<SampleImage> sampleImages = sampleImageDao.querySampleImagesByIds(sampleImageIds);
        MovieSampleImageVO vo = new MovieSampleImageVO();
        vo.setMovie(movie);
        vo.setSampleImages(sampleImages);
        return vo;
    }

}
