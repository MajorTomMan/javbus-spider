package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.ActressSeriesVo;
import com.javbus.spider.spider.service.relation.ActressSeriesRelationService;
import com.javbus.spider.spider.utils.R;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@RestController
@RequestMapping("actress/relation/series")
public class ActressSeriesRelationController {
    @Autowired
    private ActressSeriesRelationService ActressSeriesRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody ActressSeriesVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getSeries() == null || vo.getActress() == null) {
            return R.error();
        }
        if (vo.getActress().isEmpty()) {
            return R.error();
        }
        ActressSeriesRelationService.saveRelation(vo);
        return R.ok();
    }

}
