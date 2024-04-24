package com.javbus.spider.spider.controller.base;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.SampleImage;
import com.javbus.spider.spider.entity.dto.ActressesImageDTO;
import com.javbus.spider.spider.service.base.SampleImageService;
import com.javbus.spider.spider.utils.ImageUtil;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("sampleimage")
public class SampleImageController {
    @Autowired
    private SampleImageService sampleImageService;
    @Autowired
    private ImageUtil imageUtil;

    @PostMapping("save")
    public R saveSample(@RequestBody List<SampleImage> sampleImages) {
        // TODO: process POST request
        if (sampleImages == null || sampleImages.isEmpty()) {
            return R.error();
        }
        sampleImageService.saveSampleImages(sampleImages);
        return R.ok();
    }

    @GetMapping("query/id/{id}")
    public R querySampleImageById(@PathVariable Integer id) {
        SampleImage sampleImage = sampleImageService.querySampleImageById(id);
        return R.ok().put("sampleImage", sampleImage);
    }

    @PostMapping("save/sample")
    public R saveImage(@RequestBody ActressesImageDTO dto) {
        if (dto == null || dto.getActresses() == null || dto.getActresses().isEmpty() || dto.getImages() == null
                || dto.getImages().isEmpty()
                || dto.getCode() == null
                || dto.getCode().isEmpty()) {
            return R.error();
        }
        imageUtil.saveImages(dto.getImages(), dto.getActresses(), dto.getCode(),dto.getNames(),true);
        return R.ok();
    }
}
