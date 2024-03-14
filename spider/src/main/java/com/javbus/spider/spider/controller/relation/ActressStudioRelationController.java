package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.ActressStudioVo;
import com.javbus.spider.spider.service.relation.ActressStudioRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("actress/relation/studio")
public class ActressStudioRelationController {
    @Autowired
    private ActressStudioRelationService ActressStudioRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody ActressStudioVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getActress() == null || vo.getStudio() == null) {
            return R.error();
        }
        if(vo.getActress().isEmpty()){
            return R.error();
        }
        ActressStudioRelationService.saveRelation(vo);
        return R.ok();
    }
}
