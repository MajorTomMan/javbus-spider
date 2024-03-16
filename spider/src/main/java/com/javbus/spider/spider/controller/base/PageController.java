package com.javbus.spider.spider.controller.base;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.vo.PageVO;
import com.javbus.spider.spider.service.base.PageService;
import com.javbus.spider.spider.utils.R;

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
