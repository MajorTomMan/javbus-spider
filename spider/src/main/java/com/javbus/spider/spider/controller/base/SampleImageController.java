package com.javbus.spider.spider.controller.base;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.SampleImage;
import com.javbus.spider.spider.service.base.SampleImageService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("sampleimage")
public class SampleImageController {
    @Autowired
    private SampleImageService sampleImageService;
    
    @PostMapping("save")
    public R saveMovie(@RequestBody List<SampleImage> sampleImages) {
        // TODO: process POST request
        sampleImageService.saveSampleImages(sampleImages);
        return R.ok();
    }
}
