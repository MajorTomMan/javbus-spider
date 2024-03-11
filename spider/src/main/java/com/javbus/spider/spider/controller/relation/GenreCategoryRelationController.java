package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.GenreCategoryVo;
import com.javbus.spider.spider.service.relation.GenreCategoryRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("genre/relation/category")
public class GenreCategoryRelationController {
    @Autowired
    private GenreCategoryRelationService genreCategoryRelationService;

    @PostMapping("save")
    public R saveGenre(@RequestBody GenreCategoryVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getCategories() == null || vo.getGenre() == null) {
            return R.error();
        }
        genreCategoryRelationService.saveRelation(vo);
        return R.ok();
    }
}
