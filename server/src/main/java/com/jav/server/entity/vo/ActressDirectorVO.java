package com.jav.server.entity.vo;


import com.jav.server.entity.base.Director;
import com.jav.server.entity.base.Actress;

import lombok.Data;

@Data
public class ActressDirectorVO {
    Actress actress;
    Director director;
}
