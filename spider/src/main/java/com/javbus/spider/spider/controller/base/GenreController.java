package com.javbus.spider.spider.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Genre;
import com.javbus.spider.spider.service.base.GenreService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("genre")
public class GenreController {
    @Autowired
    private GenreService genreService;

    @PostMapping("save")
    public R saveGenre(@RequestBody Genre genre) {
        // TODO: process POST request
        genreService.saveGenre(genre);
        return R.ok();
    }

    @GetMapping("query/id/{id}")
    public R queryGenreById(@PathVariable Integer id) {
        Genre genre = genreService.queryGenreById(id);
        return R.ok().put("genre", genre);
    }
    @GetMapping("query/name/{name}")
    public R queryGenreByName(@PathVariable String name) {
        Genre genre = genreService.queryGenreByName(name);
        return R.ok().put("genre", genre);
    }
}
