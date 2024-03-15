package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.MovieSampleImageDTO;
import com.javbus.spider.spider.entity.vo.MovieSampleImageVO;

public interface MovieSampleImageRelationService {

    void saveRelation(MovieSampleImageDTO dto);

    MovieSampleImageVO queryRelations(Integer movieId);
    
}
