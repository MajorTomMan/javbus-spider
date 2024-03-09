package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.MovieCategoryVo;
import com.javbus.spider.spider.service.relation.MovieCategoryRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/category")
public class MovieCategoryRelationController {
    @Autowired
    private MovieCategoryRelationService movieCategoryRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieCategoryVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getCategories() == null || vo.getMovie().getCode() == null) {
            return R.error();
        }
        if(vo.getCategories().isEmpty()){
            return R.error();
        }
        movieCategoryRelationService.saveRelation(vo);
        return R.ok();
    }
}
