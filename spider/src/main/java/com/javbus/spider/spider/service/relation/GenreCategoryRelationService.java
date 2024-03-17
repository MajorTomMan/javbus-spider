package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.GenreCategoryDTO;
import com.javbus.spider.spider.entity.vo.GenreCategoryVO;

public interface GenreCategoryRelationService {

    void saveRelation(GenreCategoryDTO dto);

    GenreCategoryVO queryRelations(Integer genreId);

    GenreCategoryVO queryRelations(Integer genreId, Boolean isCensored);
    
}
