package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.MovieActressVo;
import com.javbus.spider.spider.service.relation.MovieActressRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/actress")
public class MovieActressRelationController {
    @Autowired
    private MovieActressRelationService movieActressRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieActressVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getActress() == null || vo.getMovie().getCode() == null) {
            return R.error();
        }
        movieActressRelationService.saveRelation(vo);
        return R.ok();
    }
}
