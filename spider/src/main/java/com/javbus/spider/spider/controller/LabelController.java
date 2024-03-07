package com.javbus.spider.spider.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.Label;
import com.javbus.spider.spider.service.LabelService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("label")
public class LabelController {
    @Autowired
    private LabelService labelService;
    
    @PostMapping("save")
    public R saveLabel(@RequestBody Label label) {
        // TODO: process POST request
        labelService.saveLabel(label);
        return R.ok();
    }
}
