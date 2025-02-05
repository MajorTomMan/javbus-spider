package com.jav.server.service.relation;

import com.jav.server.entity.dto.GenreCategoryDTO;
import com.jav.server.entity.vo.GenreCategoryVO;

public interface GenreCategoryRelationService {

    void saveRelation(GenreCategoryDTO dto);

    GenreCategoryVO queryRelations(Integer genreId);

    GenreCategoryVO queryRelations(Integer genreId, Boolean isCensored);
    
}
