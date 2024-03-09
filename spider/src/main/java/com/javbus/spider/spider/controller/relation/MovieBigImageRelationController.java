package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.MovieBigImageVo;
import com.javbus.spider.spider.service.relation.MovieBigImageRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/bigimage")
public class MovieBigImageRelationController {
    @Autowired
    private MovieBigImageRelationService movieBigImageRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieBigImageVo vo) {
        if (vo == null || vo.getBigImage() == null || vo.getMovie().getCode() == null) {
            return R.error();
        }
        // TODO: process POST request
        movieBigImageRelationService.saveRelaton(vo);
        return R.ok();
    }
}
