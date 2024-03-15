package com.javbus.spider.spider.controller.base;

import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.service.base.ActressService;
import com.javbus.spider.spider.utils.R;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * ActorController
 */
@RestController
@RequestMapping("actress")
public class ActressController {
    @Autowired
    private ActressService actressService;

    @RequestMapping("save")
    public R saveActress(@RequestBody List<Actress> actresses) {
        // TODO: process POST request
        if (actresses == null || actresses.isEmpty()) {
            return R.error();
        }
        actressService.saveActresses(actresses);
        return R.ok();
    }

    @GetMapping("query/id/{id}")
    public R queryActressById(@PathVariable Integer id) {
        Actress actress = actressService.queryActressById(id);
        if (actress == null) {
            return R.error().put("actress", null);
        }
        return R.ok().put("actress", actress);
    }

    @GetMapping("query/name/{name}")
    public R queryActressByName(@PathVariable String name) {
        Actress actress = actressService.queryActressByName(name);
        if (actress == null) {
            return R.error().put("actress", null);
        }
        return R.ok().put("actress", actress);
    }
}