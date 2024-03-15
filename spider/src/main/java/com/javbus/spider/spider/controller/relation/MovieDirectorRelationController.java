package com.javbus.spider.spider.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.dto.MovieDirectorDTO;
import com.javbus.spider.spider.entity.vo.MovieDirectorVO;
import com.javbus.spider.spider.service.relation.MovieDirectorRelationService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("/movie/relation/director")
public class MovieDirectorRelationController {
    @Autowired
    private MovieDirectorRelationService movieDirectorRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieDirectorDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getDirector() == null || dto.getMovie().getCode() == null) {
            return R.error();
        }
        movieDirectorRelationService.saveRelaton(dto);
        return R.ok();
    }

    @GetMapping("query/{movieId}")
    public R queryRelation(@PathVariable Integer movieId) {
        MovieDirectorVO vos = movieDirectorRelationService.queryRelations(movieId);
        return R.ok().put("vos", vos);
    }
}
