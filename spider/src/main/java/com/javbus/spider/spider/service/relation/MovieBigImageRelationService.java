package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.MovieBigImageDTO;
import com.javbus.spider.spider.entity.vo.MovieBigImageVO;

public interface MovieBigImageRelationService {

    void saveRelaton(MovieBigImageDTO dto);

    MovieBigImageVO queryRelations(Integer movieId);
    
}
