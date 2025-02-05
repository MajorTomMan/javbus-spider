package com.jav.server.service.relation;

import com.jav.server.entity.dto.ActressSeriesDTO;
import com.jav.server.entity.vo.ActressSeriesVO;

public interface ActressSeriesRelationService {

    void saveRelation(ActressSeriesDTO dto);

    ActressSeriesVO queryRelations(Integer actressId);
    
}
