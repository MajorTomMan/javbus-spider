package com.javbus.spider.spider.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.base.Series;
import com.javbus.spider.spider.service.base.SeriesService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("series")
public class SeriesController {
    @Autowired
    private SeriesService seriesService;
    
    @PostMapping("save")
    public R saveSeries(@RequestBody Series series) {
        // TODO: process POST request
        seriesService.saveSeries(series);
        return R.ok();
    }
}
