package com.javbus.spider.spider.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.Genre;
import com.javbus.spider.spider.service.GenreService;
import com.javbus.spider.spider.utils.R;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
@RequestMapping("genre")
public class GenreController {
    @Autowired
    private GenreService genreService;
    @PostMapping("save")
    public R saveGenre(@RequestBody Genre genre) {
        //TODO: process POST request
        genreService.saveGenre(genre);
        return R.ok();
    }
    
}
