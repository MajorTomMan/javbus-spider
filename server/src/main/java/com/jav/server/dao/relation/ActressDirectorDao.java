package com.jav.server.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.relation.ActressDirectorRelation;

@Mapper
public interface ActressDirectorDao {
    void addActressDirectorRelation(ActressDirectorRelation relation);

    void addActressDirectorRelations(List<ActressDirectorRelation> relations);

    void deleteActressDirectorRelation(Integer actressId, Integer directorId);

    ActressDirectorRelation queryActressDirectorRelation(Integer actressId, Integer directorId);

    List<ActressDirectorRelation> queryActressDirectorRelations(List<Integer> actressIds, Integer directorId);

    ActressDirectorRelation queryActressDirectorRelationByActressId(Integer actressId);

    void updateActressDirectorRelations(List<ActressDirectorRelation> relations);
}
