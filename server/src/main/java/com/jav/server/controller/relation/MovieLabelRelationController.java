package com.jav.server.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.dto.MovieLabelDTO;
import com.jav.server.entity.vo.MovieLabelVO;
import com.jav.server.service.relation.MovieLabelRelationService;
import com.jav.server.utils.R;

@RestController
@RequestMapping("movie/relation/label")
public class MovieLabelRelationController {
    @Autowired
    private MovieLabelRelationService movieLabelRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieLabelDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getLabel() == null || dto.getMovie().getCode() == null) {
            return R.error();
        }
        movieLabelRelationService.saveRelation(dto);
        return R.ok();
    }

    @GetMapping("query/{movieId}")
    public R queryRelation(@PathVariable Integer movieId) {
        MovieLabelVO vos = movieLabelRelationService.queryRelations(movieId);
        return R.ok().put("vos", vos);
    }
}
