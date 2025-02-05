package com.jav.server.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.dto.ActressStudioDTO;
import com.jav.server.entity.vo.ActressStudioVO;
import com.jav.server.service.relation.ActressStudioRelationService;
import com.jav.server.utils.R;

@RestController
@RequestMapping("actress/relation/studio")
public class ActressStudioRelationController {
    @Autowired
    private ActressStudioRelationService actressStudioRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody ActressStudioDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getActress() == null || dto.getStudio() == null) {
            return R.error();
        }
        if (dto.getActress().isEmpty()) {
            return R.error();
        }
        actressStudioRelationService.saveRelation(dto);
        return R.ok();
    }

    @GetMapping("query/{actressId}")
    public R queryRelation(@PathVariable Integer actressId) {
        ActressStudioVO vos = actressStudioRelationService.queryRelations(actressId);
        return R.ok().put("vos", vos);
    }
}
