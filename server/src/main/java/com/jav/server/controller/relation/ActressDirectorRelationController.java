package com.jav.server.controller.relation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.dto.ActressDirectorDTO;
import com.jav.server.entity.vo.ActressDirectorVO;
import com.jav.server.service.relation.ActressDirectorRelationService;
import com.jav.server.utils.R;

@RestController
@RequestMapping("actress/relation/director")
public class ActressDirectorRelationController {
    @Autowired
    private ActressDirectorRelationService actressDirectorRelationService;

    @PostMapping("save")
    public R saveRelation(@RequestBody ActressDirectorDTO dto) {
        // TODO: process POST request
        if (dto == null || dto.getDirector() == null || dto.getActress() == null) {
            return R.error();
        }
        if (dto.getActress().isEmpty()) {
            return R.error();
        }
        actressDirectorRelationService.saveRelation(dto);
        return R.ok();
    }
    @GetMapping("query/{actressId}")
    public R queryRelation(@PathVariable Integer actressId) {
        ActressDirectorVO vos = actressDirectorRelationService.queryRelations(actressId);
        return R.ok().put("vos", vos);
    }
}
