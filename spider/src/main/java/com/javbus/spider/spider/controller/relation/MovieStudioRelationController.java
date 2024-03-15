package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.dto.MovieStudioDTO;
import com.javbus.spider.spider.entity.vo.MovieStudioVO;
import com.javbus.spider.spider.service.relation.MovieStudioRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/studio")
public class MovieStudioRelationController {
    @Autowired
    private MovieStudioRelationService movieStudioRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieStudioDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getStudio() == null || dto.getMovie().getCode() == null) {
            return R.error();
        }
        movieStudioRelationService.saveRelation(dto);
        return R.ok();
    }

    @GetMapping("query/{movieId}")
    public R queryRelation(@PathVariable Integer movieId) {
        MovieStudioVO vos = movieStudioRelationService.queryRelations(movieId);
        return R.ok().put("vos", vos);
    }
}
