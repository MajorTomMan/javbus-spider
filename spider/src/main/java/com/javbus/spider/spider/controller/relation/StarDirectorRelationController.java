package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.StarDirectorVo;
import com.javbus.spider.spider.service.relation.StarDirectorRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("star/relation/director")
public class StarDirectorRelationController {
    @Autowired
    private StarDirectorRelationService starDirectorRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody StarDirectorVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getDirector() == null || vo.getStars() == null) {
            return R.error();
        }
        if (vo.getStars().isEmpty()) {
            return R.error();
        }
        starDirectorRelationService.saveRelation(vo);
        return R.ok();
    }
}
