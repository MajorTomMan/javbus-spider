package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.MovieActressDTO;
import com.javbus.spider.spider.entity.vo.MovieActressVO;

public interface MovieActressRelationService {

    void saveRelation(MovieActressDTO dto);

    MovieActressVO queryRelations(Integer movieId);

}
