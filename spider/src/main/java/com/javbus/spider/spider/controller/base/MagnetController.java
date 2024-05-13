/*
 * @Date: 2024-05-12 15:57:13
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-05-13 21:43:30
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\controller\base\MagnetController.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */
package com.javbus.spider.spider.controller.base;

import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Magnet;
import com.javbus.spider.spider.service.base.MagnetService;
import com.javbus.spider.spider.utils.R;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@RestController
@RequestMapping("/magnet")
public class MagnetController {
    @Autowired
    private MagnetService magnetService;

    @PostMapping("save")
    public R saveMagnet(@RequestBody Magnet magnet) {
        magnetService.save(magnet);
        return R.ok();
    }

    @PostMapping("delete")
    public R deleteMagnet(@RequestParam Integer id) {
        magnetService.delete(id);
        return R.ok();
    }

    @PostMapping("update")
    public R updateMagnet(@RequestBody Magnet magnet) {
        magnetService.update(magnet);
        return R.ok();
    }

    @GetMapping("get/{id}")
    public R getMagnetById(@PathVariable Integer id) {
        Magnet magnet = magnetService.getById(id);
        return R.ok().put("data", magnet);
    }

    @GetMapping("get")
    public R getMagnetByLink(@RequestParam String link) {
        Magnet magnet = magnetService.getByLink(link);
        return R.ok().put("data", magnet);
    }

}
