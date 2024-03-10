package com.javbus.spider.spider.controller.relation;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.StarCensorVo;
import com.javbus.spider.spider.service.relation.StarCensorRelationService;
import com.javbus.spider.spider.utils.R;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
@RequestMapping("star/relation/censor")
public class StarCensorRelationController {
    @Autowired
    private StarCensorRelationService starCensorRelationService;
    @PostMapping("save")
    public R saveRelation(@RequestBody StarCensorVo vo) {
        //TODO: process POST request
        starCensorRelationService.saveRelation(vo);
        return R.ok();
    }
    
}
