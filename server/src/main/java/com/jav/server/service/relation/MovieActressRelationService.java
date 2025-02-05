package com.jav.server.service.relation;

import com.jav.server.entity.dto.MovieActressDTO;
import com.jav.server.entity.vo.MovieActressVO;

public interface MovieActressRelationService {

    void saveRelation(MovieActressDTO dto);

    MovieActressVO queryRelations(Integer movieId);

}
