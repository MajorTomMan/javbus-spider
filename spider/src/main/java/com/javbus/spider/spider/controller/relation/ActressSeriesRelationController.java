package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.dto.ActressSeriesDTO;
import com.javbus.spider.spider.entity.vo.ActressSeriesVO;
import com.javbus.spider.spider.service.relation.ActressSeriesRelationService;
import com.javbus.spider.spider.utils.R;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@RestController
@RequestMapping("actress/relation/series")
public class ActressSeriesRelationController {
    @Autowired
    private ActressSeriesRelationService actressSeriesRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody ActressSeriesDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getSeries() == null || dto.getActress() == null) {
            return R.error();
        }
        if (dto.getActress().isEmpty()) {
            return R.error();
        }
        actressSeriesRelationService.saveRelation(dto);
        return R.ok();
    }

    @GetMapping("query/{actressId}")
    public R queryRelation(@PathVariable Integer actressId) {
        ActressSeriesVO vos = actressSeriesRelationService.queryRelations(actressId);
        return R.ok().put("vos", vos);
    }
}
