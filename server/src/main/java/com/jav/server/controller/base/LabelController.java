package com.jav.server.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.base.Label;
import com.jav.server.service.base.LabelService;
import com.jav.server.utils.R;

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

    @GetMapping("query/id/{id}")
    public R queryLabelById(@PathVariable Integer id) {
        Label label = labelService.queryLabelById(id);
        return R.ok().put("label", label);
    }

    @GetMapping("query/name/{name}")
    public R queryLabelByName(@PathVariable String name) {
        Label label = labelService.queryLabelByName(name);
        return R.ok().put("label", label);
    }
}
