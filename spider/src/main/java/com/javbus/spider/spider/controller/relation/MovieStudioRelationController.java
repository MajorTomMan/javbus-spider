package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.MovieStudioVo;
import com.javbus.spider.spider.service.relation.MovieStudioRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/studio")
public class MovieStudioRelationController {
    @Autowired
    private MovieStudioRelationService movieStudioRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieStudioVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getStudio() == null || vo.getMovie().getCode() == null) {
            return R.error();
        }
        movieStudioRelationService.saveRelation(vo);
        return R.ok();
    }
}
