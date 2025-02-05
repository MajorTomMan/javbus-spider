package com.jav.server.service.relation;

import com.jav.server.entity.dto.MovieDirectorDTO;
import com.jav.server.entity.vo.MovieDirectorVO;

public interface MovieDirectorRelationService {

    void saveRelaton(MovieDirectorDTO dto);

    MovieDirectorVO queryRelations(Integer movieId);

}
