package com.javbus.spider.spider.controller.relation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.MovieLabelVo;
import com.javbus.spider.spider.service.relation.MovieLabelRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/label")
public class MovieLabelRelationController {
    @Autowired
    private MovieLabelRelationService movieLabelRelationService;
    
    @PostMapping("save")
    public R saveRelation(@RequestBody MovieLabelVo vo) {
        // TODO: process POST request
        if(vo==null||vo.getLabel()==null||vo.getMovie().getCode()==null){
            return R.error();
        }
        movieLabelRelationService.saveRelation(vo);
        return R.ok();
    }
}
