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
        Resource resource = resourceLoader.getResource("classpath:static/image/");
        return findImage(new File(resource.getFile().getAbsolutePath()), code);
    }

    @Override
    public List<String> queryAllMovieCode(Boolean isCensored, Integer pageSize, Integer offset) {
        // TODO Auto-generated method stub
        return movieDao.queryMovieCodes(isCensored, pageSize, offset);
    }

    private List<byte[]> findImage(File file, String code) {
        if (file == null || !file.exists() || !file.isDirectory()) {
            return null;
        }
        List<byte[]> images = new ArrayList<>();
        if (file.getName().equals(code)) {
            images.addAll(findAllImage(file));
        } else {
            for (File child : file.listFiles()) {
                List<byte[]> subImages = findImage(child, code);
                if (subImages != null) {
                    images.addAll(subImages);
                }
            }
        }
        return images;
    }

    private List<byte[]> findAllImage(File directory) {
        List<byte[]> images = new ArrayList<>();
        if (directory == null || !directory.exists()) {
            return images;
        }
        File[] files = directory.listFiles();
        if (files == null) {
            return images;
        }
        for (File file : files) {
            if (file.isDirectory()) {
                images.addAll(findAllImage(file));
            } else if (file.isFile() && (file.getName().endsWith(".jpg") || file.getName().endsWith(".png"))) {
                byte[] image = readImage(file);
                if (image != null) {
                    images.add(readImage(file));
                }

            }
        }
        return images;
    }

    private byte[] readImage(File file) {
        try (FileInputStream inputStream = new FileInputStream(file)) {
            byte[] buffer = new byte[8192]; // 8KB buffer
            int bytesRead;
            List<Byte> byteList = new ArrayList<>();
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                for (int i = 0; i < bytesRead; i++) {
                    byteList.add(buffer[i]);
                }
            }
            byte[] imageData = new byte[byteList.size()];
            for (int i = 0; i < byteList.size(); i++) {
                imageData[i] = byteList.get(i);
            }
            return imageData;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

}
