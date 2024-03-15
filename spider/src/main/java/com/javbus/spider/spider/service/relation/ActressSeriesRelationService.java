package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.ActressSeriesDTO;
import com.javbus.spider.spider.entity.vo.ActressSeriesVO;

public interface ActressSeriesRelationService {

    void saveRelation(ActressSeriesDTO dto);

    ActressSeriesVO queryRelations(Integer actressId);
    
}
