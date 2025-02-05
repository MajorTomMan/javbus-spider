package com.jav.server.service.relation;

import com.jav.server.entity.dto.MovieCategoryDTO;
import com.jav.server.entity.vo.MovieCategoryVO;

public interface MovieCategoryRelationService {

    void saveRelation(MovieCategoryDTO dto);

    MovieCategoryVO queryRelations(Integer movieId);
    
}
