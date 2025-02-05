package com.jav.server.service.relation;

import com.jav.server.entity.dto.ActressDirectorDTO;
import com.jav.server.entity.vo.ActressDirectorVO;

public interface ActressDirectorRelationService {

    void saveRelation(ActressDirectorDTO dto);

    ActressDirectorVO queryRelations(Integer actressId);
    
}
