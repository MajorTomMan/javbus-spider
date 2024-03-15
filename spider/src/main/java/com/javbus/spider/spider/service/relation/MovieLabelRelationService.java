package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.MovieLabelDTO;
import com.javbus.spider.spider.entity.vo.MovieLabelVO;

public interface MovieLabelRelationService {

    void saveRelation(MovieLabelDTO dto);

    MovieLabelVO queryRelations(Integer movieId);
    
}
