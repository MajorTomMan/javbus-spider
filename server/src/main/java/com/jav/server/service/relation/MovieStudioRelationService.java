package com.jav.server.service.relation;

import com.jav.server.entity.dto.MovieStudioDTO;
import com.jav.server.entity.vo.MovieStudioVO;

public interface MovieStudioRelationService {

    void saveRelation(MovieStudioDTO dto);

    MovieStudioVO queryRelations(Integer movieId);
    
}
