package com.jav.server.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.dto.MovieSeriesDTO;
import com.jav.server.entity.vo.MovieSeriesVO;
import com.jav.server.service.relation.MovieSeriesRelationService;
import com.jav.server.utils.R;

@RestController
@RequestMapping("movie/relation/series")
public class MovieSeriesRelationController {
    @Autowired
    private MovieSeriesRelationService movieSeriesRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieSeriesDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getSeries() == null || dto.getMovie().getCode() == null) {
            return R.error();
        }
        movieSeriesRelationService.saveRelaton(dto);
        return R.ok();
    }

    @GetMapping("query/{movieId}")
    public R queryRelation(@PathVariable Integer movieId) {
        MovieSeriesVO vos = movieSeriesRelationService.queryRelations(movieId);
        return R.ok().put("vos", vos);
    }
}
