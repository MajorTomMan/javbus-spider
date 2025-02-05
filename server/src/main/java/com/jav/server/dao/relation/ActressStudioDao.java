package com.jav.server.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.relation.ActressStudioRelation;

@Mapper
public interface ActressStudioDao {
    void addActressStudioRelation(ActressStudioRelation relation);

    void deleteActressStudioRelation(Integer actressId, Integer studioId);

    void addActressStudioRelations(List<ActressStudioRelation> relations);
    ActressStudioRelation queryActressStudioRelation(Integer actressId, Integer studioId);
    List<ActressStudioRelation> queryActressStudioRelations(List<Integer> actressIds, Integer studioId);

    List<ActressStudioRelation> queryActressStudioRelationByActressId(Integer actressId);

    void updateActressStudioRelations(List<ActressStudioRelation> relations);
}
