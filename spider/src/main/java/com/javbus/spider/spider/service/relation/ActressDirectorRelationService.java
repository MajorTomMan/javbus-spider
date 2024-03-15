package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.ActressDirectorDTO;
import com.javbus.spider.spider.entity.vo.ActressDirectorVO;

public interface ActressDirectorRelationService {

    void saveRelation(ActressDirectorDTO dto);

    ActressDirectorVO queryRelations(Integer actressId);
    
}
