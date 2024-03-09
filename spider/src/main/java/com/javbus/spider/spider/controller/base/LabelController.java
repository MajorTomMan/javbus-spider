package com.javbus.spider.spider.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Label;
import com.javbus.spider.spider.service.base.LabelService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("label")
public class LabelController {
    @Autowired
    private LabelService labelService;

    @PostMapping("save")
    public R saveLabel(@RequestBody Label label) {
        // TODO: process POST request
        if (label == null) {
            return R.error();
        }
        labelService.saveLabel(label);
        return R.ok();
    }
}
