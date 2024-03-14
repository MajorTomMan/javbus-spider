package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.BigImageDao;
import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.dto.MovieActressBigImageDao;
import com.javbus.spider.spider.dao.relation.MovieBigImageDao;
import com.javbus.spider.spider.entity.base.BigImage;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.dto.BigImageDTO;
import com.javbus.spider.spider.entity.dto.ImageDTO;
import com.javbus.spider.spider.entity.relation.MovieBigImageRelation;
import com.javbus.spider.spider.entity.vo.MovieBigImageVo;
import com.javbus.spider.spider.service.relation.MovieBigImageRelationService;
import com.javbus.spider.spider.utils.ImageUtil;

@Service
public class MovieBigImageRelationServiceImpl implements MovieBigImageRelationService {
    @Autowired
    private MovieActressBigImageDao movieActressBigImageDao;
    @Autowired
    private MovieBigImageDao movieBigImageDao;
    @Autowired
    private MovieDao movieDao;
    @Autowired
    private BigImageDao bigImageDao;
    @Autowired
    private ImageUtil imageUtil;

    @Override
    public void saveRelaton(MovieBigImageVo vo) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        if (movie == null) {
            movieDao.saveMovie(vo.getMovie());
            movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        }
        BigImage bigImage = vo.getBigImage();
        BigImage bigImageResult = bigImageDao.queryBigImageByLink(bigImage.getLink());
        if (bigImageResult == null) {
            bigImageDao.saveBigImage(bigImage);
            bigImageResult = bigImageDao.queryBigImageByLink(vo.getBigImage().getLink());
        }
        MovieBigImageRelation movieBigImageRelation = movieBigImageDao.queryMovieBigImageRelation(movie.getId(),
                bigImageResult.getId());
        if (movieBigImageRelation == null) {
            MovieBigImageRelation relation = new MovieBigImageRelation();
            relation.setBigImageId(bigImageResult.getId());
            relation.setMovieId(movie.getId());
            movieBigImageDao.addMovieBigImageRelation(relation);
            List<ImageDTO> imageDTOs = movieActressBigImageDao.queryImageDao(movie.getId());
            if (imageDTOs == null || imageDTOs.isEmpty()) {
                return;
            }
            List<BigImageDTO> bigImageDTOs = imageDTOs.stream().map(imageDTO -> {
                BigImageDTO bigImageDTO = new BigImageDTO();
                String[] split = imageDTO.getLink().split("/");
                String fileName = split[split.length - 1];
                bigImageDTO.setFileName(fileName);
                bigImageDTO.setName(imageDTO.getName());
                bigImageDTO.setCode(imageDTO.getCode());
                if (!imageUtil.checkImageIsExists(bigImageDTO)) {
                    byte[] data = imageUtil.download(imageDTO.getLink());
                    bigImageDTO.setBigImage(data);
                } else {
                    bigImageDTO.setBigImage(null);
                }
                return bigImageDTO;
            }).filter(dto -> dto.getBigImage() != null).collect(Collectors.toList());
            imageUtil.saveBigImage(bigImageDTOs);
        }
    }

}
