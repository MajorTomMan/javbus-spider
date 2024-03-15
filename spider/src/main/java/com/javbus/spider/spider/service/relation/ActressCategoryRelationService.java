package com.javbus.spider.spider.service.relation;


import com.javbus.spider.spider.entity.dto.ActressCategoryDTO;
import com.javbus.spider.spider.entity.vo.ActressCategoryVO;

public interface ActressCategoryRelationService {

    void saveRelation(ActressCategoryDTO dto);

    ActressCategoryVO queryRelations(Integer actressId);
    
}
