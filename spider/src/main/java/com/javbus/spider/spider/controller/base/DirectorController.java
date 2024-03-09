package com.javbus.spider.spider.controller.base;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.service.base.DirectorService;
import com.javbus.spider.spider.utils.R;

import org.springframework.beans.factory.annotation.Autowired;
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

}
