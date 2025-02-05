package com.jav.server.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.base.Series;
import com.jav.server.service.base.SeriesService;
import com.jav.server.utils.R;

@RestController
@RequestMapping("series")
public class SeriesController {
    @Autowired
    private SeriesService seriesService;

    @PostMapping("save")
    public R saveSeries(@RequestBody Series series) {
        // TODO: process POST request
        if (series == null) {
            return R.error();
        }
        seriesService.saveSeries(series);
        return R.ok();
    }

    @GetMapping("query/id/{id}")
    public R querySampleImageById(@PathVariable Integer id) {
        Series series = seriesService.querySeriesById(id);
        return R.ok().put("series", series);
    }
    @GetMapping("query/name/{name}")
    public R querySampleImageByName(@PathVariable String name) {
        Series series = seriesService.querySeriesByName(name);
        return R.ok().put("series", series);
    }
}
