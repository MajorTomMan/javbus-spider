/*
 * @Date: 2024-04-24 20:38:18
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-06-20 08:09:38
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\controller\base\BigImageController.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */

package com.jav.server.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.base.BigImage;
import com.jav.server.entity.dto.ActressesImageDTO;
import com.jav.server.service.base.BigImageService;
import com.jav.server.utils.ImageUtil;
import com.jav.server.utils.R;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@RestController
@RequestMapping("bigimage")
public class BigImageController {
    @Autowired
    private BigImageService bigImageService;
    @Autowired
    private ImageUtil imageUtil;

    @PostMapping("save")
    public R saveBigImage(@RequestBody BigImage bigImage) {
        // TODO: process POST request
        if (bigImage == null) {
            return R.error();
        }
        bigImageService.saveBigImage(bigImage);
        return R.ok();
    }

    @GetMapping("query/id/{id}")
    public R queryBigImageByLink(@PathVariable Integer id) {
        BigImage image = bigImageService.queryBigImageById(id);
        return R.ok().put("bigImage", image);
    }

    @PostMapping("save/local")
    public R saveImage(@RequestBody ActressesImageDTO dto) {
        if (dto == null || dto.getActresses() == null || dto.getActresses().isEmpty() || dto.getImages() == null
                || dto.getImages().isEmpty()
                || dto.getCode() == null
                || dto.getCode().isEmpty()) {
            return R.error();
        }

        imageUtil.saveImages(dto.getImages(), dto.getActresses(), dto.getCode(), dto.getNames(), true);
        return R.ok();
    }
}
