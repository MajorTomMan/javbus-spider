package com.javbus.spider.spider.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Studio;
import com.javbus.spider.spider.service.base.StudioService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("studio")
public class StudioController {
    @Autowired
    private StudioService studioService;

    @PostMapping("save")
    public R saveStudio(@RequestBody Studio studio) {
        // TODO: process POST request
        if (studio == null) {
            return R.error();
        }
        studioService.saveStudio(studio);
        return R.ok();
    }
}
