package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.StarStudioVo;
import com.javbus.spider.spider.service.relation.StarStudioRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("star/relation/studio")
public class StarStudioRelationController {
    @Autowired
    private StarStudioRelationService starStudioRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody StarStudioVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getStars() == null || vo.getStudio() == null) {
            return R.error();
        }
        if(vo.getStars().isEmpty()){
            return R.error();
        }
        starStudioRelationService.saveRelation(vo);
        return R.ok();
    }
}
