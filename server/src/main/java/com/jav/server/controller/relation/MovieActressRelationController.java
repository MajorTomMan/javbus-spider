package com.jav.server.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.dto.MovieActressDTO;
import com.jav.server.entity.vo.MovieActressVO;
import com.jav.server.service.relation.MovieActressRelationService;
import com.jav.server.utils.R;

@RestController
@RequestMapping("movie/relation/actress")
public class MovieActressRelationController {
    @Autowired
    private MovieActressRelationService movieActressRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieActressDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getActress() == null || dto.getMovie().getCode() == null) {
            return R.error();
        }
        movieActressRelationService.saveRelation(dto);
        return R.ok();
    }

    @GetMapping("query/{movieId}")
    public R queryRelation(@PathVariable Integer movieId) {
        MovieActressVO vos = movieActressRelationService.queryRelations(movieId);
        return R.ok().put("vos", vos);
    }
}
