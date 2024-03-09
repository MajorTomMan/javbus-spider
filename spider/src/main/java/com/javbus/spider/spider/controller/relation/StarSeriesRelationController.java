package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.StarSeriesVo;
import com.javbus.spider.spider.service.relation.StarSeriesRelationService;
import com.javbus.spider.spider.utils.R;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@RestController
@RequestMapping("star/relation/series")
public class StarSeriesRelationController {
    @Autowired
    private StarSeriesRelationService starSeriesRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody StarSeriesVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getSeries() == null || vo.getStars() == null) {
            return R.error();
        }
        if (vo.getStars().isEmpty()) {
            return R.error();
        }
        starSeriesRelationService.saveRelation(vo);
        return R.ok();
    }

}
