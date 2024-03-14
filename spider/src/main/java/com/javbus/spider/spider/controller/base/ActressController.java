package com.javbus.spider.spider.controller.base;

import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.service.base.ActressService;
import com.javbus.spider.spider.utils.R;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * ActorController
 */
@RestController
@RequestMapping("actress")
public class ActressController {
    @Autowired
    private ActressService ActressService;

    @RequestMapping("save")
    public R saveActress(@RequestBody List<Actress> actresses) {
        // TODO: process POST request
        if (actresses == null || actresses.isEmpty()) {
            return R.error();
        }
        ActressService.saveActresses(actresses);
        return R.ok();
    }
}