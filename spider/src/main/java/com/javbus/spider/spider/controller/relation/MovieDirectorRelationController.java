package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.MovieDirectorVo;
import com.javbus.spider.spider.service.relation.MovieDirectorRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("/movie/relation/director")
public class MovieDirectorRelationController {
    @Autowired
    private MovieDirectorRelationService movieDirectorRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieDirectorVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getDirector() == null || vo.getMovie().getCode() == null ) {
            return R.error();
        }
        movieDirectorRelationService.saveRelaton(vo);
        return R.ok();
    }
}
