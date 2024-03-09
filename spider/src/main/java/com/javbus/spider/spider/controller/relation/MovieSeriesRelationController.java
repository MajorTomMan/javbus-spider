package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.MovieSeriesVo;
import com.javbus.spider.spider.service.relation.MovieSeriesRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/series")
public class MovieSeriesRelationController {
    @Autowired
    private MovieSeriesRelationService movieSeriesRelationService;
    
    @PostMapping("save")
    public R saveRelation(@RequestBody MovieSeriesVo vo) {
        // TODO: process POST request
        movieSeriesRelationService.saveRelaton(vo);
        return R.ok();
    }
}
