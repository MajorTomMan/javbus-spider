package com.javbus.spider.spider.service.relation;

import com.javbus.spider.spider.entity.dto.MovieDirectorDTO;
import com.javbus.spider.spider.entity.vo.MovieDirectorVO;

public interface MovieDirectorRelationService {

    void saveRelaton(MovieDirectorDTO dto);

    MovieDirectorVO queryRelations(Integer movieId);

}
