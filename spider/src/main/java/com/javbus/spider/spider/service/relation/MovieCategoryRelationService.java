package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.MovieCategoryDTO;
import com.javbus.spider.spider.entity.vo.MovieCategoryVO;

public interface MovieCategoryRelationService {

    void saveRelation(MovieCategoryDTO dto);

    MovieCategoryVO queryRelations(Integer movieId);
    
}
