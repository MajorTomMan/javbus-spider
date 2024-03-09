package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.StarCategoryVo;
import com.javbus.spider.spider.utils.R;
import com.javbus.spider.spider.service.relation.StarCategoryRelationService;

@RestController
@RequestMapping("star/relation/category")
public class StarCategoryRelationController {
    @Autowired
    private StarCategoryRelationService starCategoryRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody StarCategoryVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getCategories() == null || vo.getStars() == null) {
            return R.error();
        }
        if (vo.getCategories().isEmpty()) {
            return R.error();
        }
        if (vo.getStars().isEmpty()) {
            return R.error();
        }
        starCategoryRelationService.saveRelation(vo);
        return R.ok();
    }
}
