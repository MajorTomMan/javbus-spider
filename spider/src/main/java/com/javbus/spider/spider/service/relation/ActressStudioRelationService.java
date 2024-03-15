package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.ActressStudioDTO;
import com.javbus.spider.spider.entity.vo.ActressStudioVO;

public interface ActressStudioRelationService {

    void saveRelation(ActressStudioDTO dto);

    ActressStudioVO queryRelations(Integer actressId);
    
}
