package com.jav.server.service.relation;

import com.jav.server.entity.dto.MovieSampleImageDTO;
import com.jav.server.entity.vo.MovieSampleImageVO;

public interface MovieSampleImageRelationService {

    void saveRelation(MovieSampleImageDTO dto);

    MovieSampleImageVO queryRelations(Integer movieId);
    
}
