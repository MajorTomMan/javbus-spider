package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.ActressCategoryVo;
import com.javbus.spider.spider.utils.R;
import com.javbus.spider.spider.service.relation.ActressCategoryRelationService;

@RestController
@RequestMapping("actress/relation/category")
public class ActressCategoryRelationController {
    @Autowired
    private ActressCategoryRelationService ActressCategoryRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody ActressCategoryVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getCategories() == null || vo.getActress() == null) {
            return R.error();
        }
        if (vo.getCategories().isEmpty()) {
            return R.error();
        }
        if (vo.getActress().isEmpty()) {
            return R.error();
        }
        ActressCategoryRelationService.saveRelation(vo);
        return R.ok();
    }
}
