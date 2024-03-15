package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.MovieStudioDTO;
import com.javbus.spider.spider.entity.vo.MovieStudioVO;

public interface MovieStudioRelationService {

    void saveRelation(MovieStudioDTO dto);

    MovieStudioVO queryRelations(Integer movieId);
    
}
