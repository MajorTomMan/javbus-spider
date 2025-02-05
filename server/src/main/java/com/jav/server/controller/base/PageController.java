package com.jav.server.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jav.server.entity.vo.PageVO;
import com.jav.server.service.base.PageService;
import com.jav.server.utils.R;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;


@RestController
@RequestMapping("page")
public class PageController {
    @Autowired
    private PageService pageService;
    @GetMapping("query/id/{movieId}")
    public R queryPage(@PathVariable Integer movieId) {
        PageVO page=pageService.queryPageByMovieId(movieId);
        return R.ok().put("page",page);
    }
    
}
