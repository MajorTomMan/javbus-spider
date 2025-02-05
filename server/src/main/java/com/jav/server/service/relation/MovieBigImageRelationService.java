package com.jav.server.service.relation;

import com.jav.server.entity.dto.MovieBigImageDTO;
import com.jav.server.entity.vo.MovieBigImageVO;

public interface MovieBigImageRelationService {

    void saveRelaton(MovieBigImageDTO dto);

    MovieBigImageVO queryRelations(Integer movieId);
    
}
