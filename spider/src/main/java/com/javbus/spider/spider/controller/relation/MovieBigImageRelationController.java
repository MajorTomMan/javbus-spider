package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.dto.MovieBigImageDTO;
import com.javbus.spider.spider.entity.vo.MovieBigImageVO;
import com.javbus.spider.spider.service.relation.MovieBigImageRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("movie/relation/bigimage")
public class MovieBigImageRelationController {
    @Autowired
    private MovieBigImageRelationService movieBigImageRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieBigImageDTO dto) {
        if (dto == null || dto.getBigImage() == null || dto.getMovie().getCode() == null) {
            return R.error();
        }
        // TODO: process POST request
        movieBigImageRelationService.saveRelaton(dto);
        return R.ok();
    }

    @GetMapping("query/{movieId}")
    public R queryRelation(@PathVariable Integer movieId) {
        MovieBigImageVO vos = movieBigImageRelationService.queryRelations(movieId);
        return R.ok().put("vos", vos);
    }
}
