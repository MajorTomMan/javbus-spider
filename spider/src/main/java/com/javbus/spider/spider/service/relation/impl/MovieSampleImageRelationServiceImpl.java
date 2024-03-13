package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.SampleImageDao;
import com.javbus.spider.spider.dao.dto.MovieStarSampleImageDao;
import com.javbus.spider.spider.dao.relation.MovieSampleImageDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.dto.ImageDTO;
import com.javbus.spider.spider.entity.dto.SampleImageDTO;
import com.javbus.spider.spider.entity.relation.MovieSampleImageRelation;
import com.javbus.spider.spider.entity.vo.MovieSampleImageVo;
import com.javbus.spider.spider.service.relation.MovieSampleImageRelationService;
import com.javbus.spider.spider.utils.ImageUtil;

@Service
public class MovieSampleImageRelationServiceImpl implements MovieSampleImageRelationService {
    @Autowired
    private MovieStarSampleImageDao movieStarSampleImageDao;
    @Autowired
    private MovieSampleImageDao movieSampleImageDao;
    @Autowired
    private SampleImageDao sampleImageDao;
    @Autowired
    private MovieDao movieDao;
    @Autowired
    private ImageUtil imageUtil;

    @Override
    public void saveRelation(MovieSampleImageVo vo) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        if (movie == null) {
            movieDao.saveMovie(vo.getMovie());
            movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        }
        List<Integer> sampleImageIds = sampleImageDao.querySampleImageIdsByLinks(vo.getSampleImages());
        if (sampleImageIds == null || sampleImageIds.isEmpty()) {
            sampleImageDao.saveSampleImages(vo.getSampleImages());
            sampleImageIds = sampleImageDao.querySampleImageIdsByLinks(vo.getSampleImages());
        }
        List<MovieSampleImageRelation> movieSampleImageRelations = movieSampleImageDao.queryMovieSampleImageRelatios(movie.getId(), sampleImageIds);
        if(movieSampleImageRelations==null||movieSampleImageRelations.isEmpty()){
            final Movie final_movie = movie;
            List<MovieSampleImageRelation> relations = sampleImageIds.stream().map((id) -> {
                MovieSampleImageRelation relation = new MovieSampleImageRelation();
                relation.setMovieId(final_movie.getId());
                relation.setSampleImageId(id);
                return relation;
            }).collect(Collectors.toList());
            movieSampleImageDao.addMovieSampleImageRelations(relations);
            List<ImageDTO> imageDTOs = movieStarSampleImageDao.queryImageDao(movie.getId());
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
            }).filter(dto -> dto.getSampleImage() != null).collect(Collectors.toList());
            imageUtil.saveSampleImage(sampleImageDTOs);
        }
    }

}
