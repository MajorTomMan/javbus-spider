/*
 * @Date: 2024-05-12 16:09:13
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-05-13 20:53:13
 * @FilePath: \spider\src\main\java\com\javbus\spider\spider\service\base\impl\MagnetServiceImpl.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */
package com.jav.server.service.base.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jav.server.dao.base.MagnetDao;
import com.jav.server.entity.base.Magnet;
import com.jav.server.service.base.MagnetService;

@Service
public class MagnetServiceImpl implements MagnetService{
    @Autowired
    private MagnetDao dao;

    @Override
    public void save(Magnet magnet) {
        dao.saveMagnet(magnet);
    }

    @Override
    public void delete(Integer id) {
        dao.deleteMagnet(id);
    }

    @Override
    public void update(Magnet magnet) {
        dao.updateMagnet(magnet);
    }

    @Override
    public Magnet getById(Integer id) {
        return dao.queryMagnetById(id);
    }

    @Override
    public Magnet getByLink(String link) {
        return dao.queryMagnetByLink(link);
    }

    @Override
    public List<Magnet> getByLinks(List<String> links) {
        return dao.queryMagnets(links);
    }

    @Override
    public List<Integer> getIdsByLinks(List<String> links) {
        return dao.queryMagnetIdsByLinks(links);
    }
}
