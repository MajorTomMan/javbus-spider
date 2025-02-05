package com.jav.server.service.relation;


import com.jav.server.entity.dto.ActressCategoryDTO;
import com.jav.server.entity.vo.ActressCategoryVO;

public interface ActressCategoryRelationService {

    void saveRelation(ActressCategoryDTO dto);

    ActressCategoryVO queryRelations(Integer actressId);
    
}
