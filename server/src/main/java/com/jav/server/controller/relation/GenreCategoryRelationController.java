package com.jav.server.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.dto.GenreCategoryDTO;
import com.jav.server.entity.vo.GenreCategoryVO;
import com.jav.server.service.relation.GenreCategoryRelationService;
import com.jav.server.utils.R;

@RestController
@RequestMapping("genre/relation/category")
public class GenreCategoryRelationController {
    @Autowired
    private GenreCategoryRelationService genreCategoryRelationService;

    @PostMapping("/save")
    public R saveGenre(@RequestBody GenreCategoryDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getCategories() == null || dto.getGenre() == null) {
            return R.error();
        }
        genreCategoryRelationService.saveRelation(dto);
        return R.ok();
    }
    @GetMapping("query/{isCensored}/{genreId}")
    public R queryRelation(@PathVariable Integer genreId,@PathVariable Boolean isCensored) {
        GenreCategoryVO vos = genreCategoryRelationService.queryRelations(genreId,isCensored);
        return R.ok().put("vos", vos);
    }
}
