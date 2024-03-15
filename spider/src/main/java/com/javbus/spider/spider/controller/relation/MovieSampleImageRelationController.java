package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.dto.MovieSampleImageDTO;
import com.javbus.spider.spider.entity.vo.MovieSampleImageVO;
import com.javbus.spider.spider.service.relation.MovieSampleImageRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/sampleimage")
public class MovieSampleImageRelationController {
    @Autowired
    private MovieSampleImageRelationService movieSampleImageRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieSampleImageDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getSampleImages() == null || dto.getMovie().getCode() == null) {
            return R.error();
        }
        if (dto.getSampleImages().isEmpty()) {
            return R.error();
        }
        movieSampleImageRelationService.saveRelation(dto);
        return R.ok();
    }

    @GetMapping("query/{movieId}")
    public R queryRelation(@PathVariable Integer movieId) {
        MovieSampleImageVO vos = movieSampleImageRelationService.queryRelations(movieId);
        return R.ok().put("vos", vos);
    }
}
