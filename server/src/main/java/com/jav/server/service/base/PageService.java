package com.jav.server.service.base;

import com.jav.server.entity.vo.PageVO;

public interface PageService {
    PageVO queryPageByMovieId(Integer movieId);
}
