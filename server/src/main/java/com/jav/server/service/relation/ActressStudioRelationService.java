package com.jav.server.service.relation;

import com.jav.server.entity.dto.ActressStudioDTO;
import com.jav.server.entity.vo.ActressStudioVO;

public interface ActressStudioRelationService {

    void saveRelation(ActressStudioDTO dto);

    ActressStudioVO queryRelations(Integer actressId);
    
}
