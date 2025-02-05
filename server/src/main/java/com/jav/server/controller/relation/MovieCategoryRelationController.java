package com.jav.server.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.dto.MovieCategoryDTO;
import com.jav.server.entity.vo.MovieCategoryVO;
import com.jav.server.service.relation.MovieCategoryRelationService;
import com.jav.server.utils.R;

@RestController
@RequestMapping("movie/relation/category")
public class MovieCategoryRelationController {
    @Autowired
    private MovieCategoryRelationService movieCategoryRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieCategoryDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getCategories() == null || dto.getMovie().getCode() == null) {
            return R.error();
        }
        if (dto.getCategories().isEmpty()) {
            return R.error();
        }
        movieCategoryRelationService.saveRelation(dto);
        return R.ok();
    }

    @GetMapping("query/{movieId}")
    public R queryRelation(@PathVariable Integer movieId) {
        MovieCategoryVO vos = movieCategoryRelationService.queryRelations(movieId);
        return R.ok().put("vos", vos);
    }
}
