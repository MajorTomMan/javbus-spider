package com.jav.server.controller.base;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.base.Director;
import com.jav.server.service.base.DirectorService;
import com.jav.server.utils.R;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@RestController
@RequestMapping("director")
public class DirectorController {
    @Autowired
    private DirectorService directorService;

    @PostMapping("save")
    public R saveDirectory(@RequestBody Director director) {
        // TODO: process POST request
        if (director == null) {
            return R.error();
        }
        directorService.saveDirector(director);
        return R.ok();
    }
    @GetMapping("query/id/{id}")
    public R queryDirectorById(@PathVariable Integer id){
        Director director=directorService.queryDirectorById(id);
        return R.ok().put("director", director);
    }
}
