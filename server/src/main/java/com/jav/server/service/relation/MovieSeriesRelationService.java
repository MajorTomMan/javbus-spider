package com.jav.server.service.relation;

import com.jav.server.entity.dto.MovieSeriesDTO;
import com.jav.server.entity.vo.MovieSeriesVO;

public interface MovieSeriesRelationService {

    void saveRelaton(MovieSeriesDTO dto);

    MovieSeriesVO queryRelations(Integer movieId);
    
}
