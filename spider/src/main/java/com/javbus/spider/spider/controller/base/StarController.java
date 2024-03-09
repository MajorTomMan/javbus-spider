package com.javbus.spider.spider.controller.base;

import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Star;
import com.javbus.spider.spider.service.base.StarService;
import com.javbus.spider.spider.utils.R;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * ActorController
 */
@RestController
@RequestMapping("star")
public class StarController {
    @Autowired
    private StarService starService;

    @RequestMapping("save")
    public R saveStar(@RequestBody List<Star> stars) {
        // TODO: process POST request
        if (stars == null || stars.isEmpty()) {
            return R.error();
        }
        starService.saveStars(stars);
        return R.ok();
    }
}