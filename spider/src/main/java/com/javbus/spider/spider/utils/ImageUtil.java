package com.javbus.spider.spider.utils;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import lombok.extern.log4j.Log4j2;

@Log4j2
@Component
public class ImageUtil {
    private String imageFolder = "./images/";
    @Autowired
    private RestTemplate restTemplate;

    public List<byte[]> download(List<String> links) {
        if (links == null || links.isEmpty()) {
            return null;
        }
        List<byte[]> images = new ArrayList<>();
        for (String link : links) {
            ResponseEntity<byte[]> image = restTemplate.getForEntity(link, byte[].class);
            images.add(image.getBody());
        }
        return images;
    }

    public byte[] download(String link) {
        if (link == null) {
            return null;
        }
        ResponseEntity<byte[]> image = restTemplate.getForEntity(link, byte[].class);
        return image.getBody();
    }

    public void saveBigImage(byte[] image, String path, String fileName) {
        save(image, path, fileName,true);
    }

    public void saveBigImages(List<byte[]> images, String path, String fileName) {
        for (byte[] image : images) {
            save(image, path, fileName,true);
        }
    }

    public void saveSampleImage(byte[] image, String path, String fileName) {
        save(image, path, fileName,false);
    }

    public void saveSampleImage(List<byte[]> images, String path, String fileName) {
        for (byte[] image : images) {
            save(image, path, fileName,false);
        }
    }

    private void save(byte[] image, String path,String fileName,Boolean isBigImage) {
        log.info("image store folder is " + path);
        File folder=null;
        if(isBigImage){
            folder = new File(imageFolder + File.separator + path+"/"+"bigimage/");
        }
        else{
            folder = new File(imageFolder + File.separator + path+"/"+"sample/");
        }
        if (!checkImageFolderIsExists(path)) {
            log.info("image store folder " + path + " not exists");
            folder.mkdirs();
            log.info("image store folder " + path + " created");
        } else {
            log.info("image store folder " + path + " exists");
        }
        if (checkImageIsExists(folder.getAbsolutePath()+File.separator+fileName, fileName)) {
            log.info("image " + imageFolder + File.separator + path + File.separator + fileName + " exists");
            return;
        }
        try (FileOutputStream fos = new FileOutputStream(new File(folder.getAbsolutePath()+"/"+fileName))) {
            fos.write(image);
            log.info("image " + fileName + " downloaded");
            log.info("image store path is " + path + fileName);
        } catch (IOException e) {
            log.error("image " + fileName + " download failed");
            log.error("reason:" + e.getMessage());
        }
    }

    public boolean checkImageFolderIsExists(String path) {
        File file = new File(path);
        if (file.exists()) {
            log.info("image " + path + " was exists");
            return true;
        }
        return false;
    }

    public boolean checkImageIsExists(String path, String fileName) {
        File file = new File(path + File.separator + fileName);
        if (file.exists()) {
            log.info("image " + file.getAbsolutePath() + " was exists");
            return true;
        }
        return false;
    }
}
