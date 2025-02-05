package com.jav.server.service.relation;

import com.jav.server.entity.dto.MovieLabelDTO;
import com.jav.server.entity.vo.MovieLabelVO;

public interface MovieLabelRelationService {

    void saveRelation(MovieLabelDTO dto);

    MovieLabelVO queryRelations(Integer movieId);
    
}
