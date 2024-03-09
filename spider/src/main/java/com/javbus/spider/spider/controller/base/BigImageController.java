package com.javbus.spider.spider.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.BigImage;
import com.javbus.spider.spider.service.base.BigImageService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("bigimage")
public class BigImageController {
    @Autowired
    private BigImageService bigImageService;

    @PostMapping("save")
    public R saveBigImage(@RequestBody BigImage bigImage) {
        // TODO: process POST request
        if (bigImage == null) {
            return R.error();
        }
        bigImageService.saveBigImage(bigImage);
        return R.ok();
    }
}
