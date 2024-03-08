package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.MovieSampleImageVo;
import com.javbus.spider.spider.service.relation.MovieSampleImageRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/sampleimage")
public class MovieSampleImageRelationController {
    @Autowired
    private MovieSampleImageRelationService movieSampleImageRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieSampleImageVo vo) {
        // TODO: process POST request
        movieSampleImageRelationService.saveRelation(vo);
        return R.ok();
    }
}
