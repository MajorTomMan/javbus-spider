package com.jav.server.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.base.Studio;
import com.jav.server.service.base.StudioService;
import com.jav.server.utils.R;




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

    @GetMapping("query/id/{id}")
    public R querySampleImageById(@PathVariable Integer id) {
        Studio studio = studioService.queryStudioById(id);
        return R.ok().put("studio", studio);
    }

    @GetMapping("query/name/{name}")
    public R querySampleImageByName(@PathVariable String name) {
        Studio studio = studioService.queryStudioByName(name);
        return R.ok().put("studio", studio);
    }
}
