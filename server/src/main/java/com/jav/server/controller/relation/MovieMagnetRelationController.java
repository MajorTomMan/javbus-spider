package com.jav.server.controller.relation;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.dto.MovieMagnetDTO;
import com.jav.server.service.relation.MovieMagnetRelationService;
import com.jav.server.utils.R;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@RestController
@RequestMapping("/movie/relation/magnet")
public class MovieMagnetRelationController {
    @Autowired
    private MovieMagnetRelationService movieMagnetRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody MovieMagnetDTO dto) {
        // TODO: process POST request
        movieMagnetRelationService.saveRelation(dto);
        return R.ok();
    }

}
