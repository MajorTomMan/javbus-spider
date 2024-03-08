package com.javbus.spider.spider.controller.base;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.service.base.MovieService;
import com.javbus.spider.spider.utils.R;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
@RequestMapping("movie")
public class MovieController {
    @Autowired
    private MovieService movieService;
    @PostMapping("save")
    public R saveMovie(@RequestBody Movie movie) {
        //TODO: process POST request
        movieService.saveMovie(movie);
        return R.ok();
    }
    
}
