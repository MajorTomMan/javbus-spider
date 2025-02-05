package com.jav.server.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.dto.ActressCategoryDTO;
import com.jav.server.entity.vo.ActressCategoryVO;
import com.jav.server.utils.R;
import com.jav.server.service.relation.ActressCategoryRelationService;

@RestController
@RequestMapping("actress/relation/category")
public class ActressCategoryRelationController {
    @Autowired
    private ActressCategoryRelationService actressCategoryRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody ActressCategoryDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getCategories() == null || dto.getActress() == null) {
            return R.error();
        }
        if (dto.getCategories().isEmpty()) {
            return R.error();
        }
        if (dto.getActress().isEmpty()) {
            return R.error();
        }
        actressCategoryRelationService.saveRelation(dto);
        return R.ok();
    }

    @GetMapping("query/{actressId}")
    public R queryRelation(@PathVariable Integer actressId) {
        ActressCategoryVO vos = actressCategoryRelationService.queryRelations(actressId);
        return R.ok().put("vos", vos);
    }
}
