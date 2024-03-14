package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.ActressDirectorVo;
import com.javbus.spider.spider.service.relation.ActressDirectorRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("actress/relation/director")
public class ActressDirectorRelationController {
    @Autowired
    private ActressDirectorRelationService ActressDirectorRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody ActressDirectorVo vo) {
        // TODO: process POST request
        if (vo == null || vo.getDirector() == null || vo.getActress() == null) {
            return R.error();
        }
        if (vo.getActress().isEmpty()) {
            return R.error();
        }
        ActressDirectorRelationService.saveRelation(vo);
        return R.ok();
    }
}
