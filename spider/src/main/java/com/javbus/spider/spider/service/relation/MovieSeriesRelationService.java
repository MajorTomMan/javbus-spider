package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.MovieSeriesDTO;
import com.javbus.spider.spider.entity.vo.MovieSeriesVO;

public interface MovieSeriesRelationService {

    void saveRelaton(MovieSeriesDTO dto);

    MovieSeriesVO queryRelations(Integer movieId);
    
}
