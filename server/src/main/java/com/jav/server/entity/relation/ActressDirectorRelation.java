package com.jav.server.entity.relation;

import lombok.Data;

@Data
public class ActressDirectorRelation {
    private Integer id;
    private Integer actressId;
    private Integer directorId;
}
