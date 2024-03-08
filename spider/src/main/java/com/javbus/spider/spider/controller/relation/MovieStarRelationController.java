package com.javbus.spider.spider.controller.relation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.MovieStarVo;
import com.javbus.spider.spider.service.relation.MovieStarRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/star")
public class MovieStarRelationController {
    @Autowired
    private MovieStarRelationService movieStarRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieStarVo vo) {
        // TODO: process POST request
        movieStarRelationService.saveRelation(vo);
        return R.ok();
    }
}
