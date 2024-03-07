package com.javbus.spider.spider.controller;

import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.Star;
import com.javbus.spider.spider.service.StarService;
import com.javbus.spider.spider.utils.R;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;


/**
 * ActorController
 */
@RestController
@RequestMapping("/star")
public class StarController {
    @Autowired
    private StarService starService;
    @RequestMapping("save")
    public R saveStar(@RequestBody Star star) {
        //TODO: process POST request
        starService.saveStar(star);
        return R.ok();
    }
}