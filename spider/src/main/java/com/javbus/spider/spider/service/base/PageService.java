package com.javbus.spider.spider.service.base;

import com.javbus.spider.spider.entity.vo.PageVO;

public interface PageService {
    PageVO queryPageByMovieId(Integer movieId);
}
