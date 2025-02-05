package com.jav.server.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.dto.MovieSampleImageDTO;
import com.jav.server.entity.vo.MovieSampleImageVO;
import com.jav.server.service.relation.MovieSampleImageRelationService;
import com.jav.server.utils.R;

@RestController
@RequestMapping("movie/relation/sampleimage")
public class MovieSampleImageRelationController {
    @Autowired
    private MovieSampleImageRelationService movieSampleImageRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieSampleImageDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getSampleImages() == null || dto.getMovie().getCode() == null) {
            return R.error();
        }
        if (dto.getSampleImages().isEmpty()) {
            return R.error();
        }
        movieSampleImageRelationService.saveRelation(dto);
        return R.ok();
    }

    @GetMapping("query/{movieId}")
    public R queryRelation(@PathVariable Integer movieId) {
        MovieSampleImageVO vos = movieSampleImageRelationService.queryRelations(movieId);
        return R.ok().put("vos", vos);
    }
}
