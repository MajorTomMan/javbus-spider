package com.javbus.spider.spider.service.base.impl;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.service.base.ImageService;

@Service
public class ImageServiceImpl implements ImageService {
    @Autowired
    private ResourceLoader resourceLoader;
    @Autowired
    private MovieDao movieDao;
    @Override
    public List<byte[]> getImagesByCode(String code) throws IOException {
        // TODO Auto-generated method stub
        Resource resource = resourceLoader.getResource("classpath:static/images/");
        return findImage(new File(resource.getFile().getAbsolutePath()), code);
    }
    @Override
    public List<String> queryAllMovieCode(Boolean isCensored, Integer pageSize, Integer offset) {
        // TODO Auto-generated method stub
        return movieDao.queryMovieCodes(isCensored,pageSize,offset);
    }

    private List<byte[]> findImage(File file, String code) {
        if (file == null || !file.exists() || !file.isDirectory()) {
            return null;
        }
        List<byte[]> images = new ArrayList<>();
        for (File child : file.listFiles()) {
            if (child.getName().equals(code)) {
                for(File children: child.listFiles()){
                    if(children.getName().endsWith(".jpg")){
                        byte[] data=readImage(children);
                        images.add(data);
                    }
                }
                return images;
            }
            if(child.isDirectory()){
                List<byte[]> subImages = findImage(child, code);
                if (subImages != null) {
                    images.addAll(subImages);
                }
            }
        }
        return null;
    }

    private byte[] readImage(File file) {
        try (FileInputStream inputStream = new FileInputStream(file)) {
            byte[] data = new byte[inputStream.available()];
            int bytesRead = inputStream.read(data);
            if (bytesRead == -1) {
                // 读取失败，返回空数组
                return new byte[0];
            } else {
                // 读取成功，返回读取的数据
                return data;
            }
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }



}
