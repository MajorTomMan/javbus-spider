package com.javbus.spider.spider.utils;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import lombok.extern.log4j.Log4j2;

@Log4j2
@Component
public class ImageUtil {
    @Autowired
    private ResourceLoader resourceLoader;
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
        try {
            save(image, path, fileName,true);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    public void saveBigImages(List<byte[]> images, String path, String fileName) {
        for (byte[] image : images) {
            try {
                save(image, path, fileName,true);
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    public void saveSampleImage(byte[] image, String path, String fileName) {
        try {
            save(image, path, fileName,false);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    public void saveSampleImage(List<byte[]> images, String path, String fileName) {
        for (byte[] image : images) {
            try {
                save(image, path, fileName,false);
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    private void save(byte[] image, String path, String fileName, Boolean isBigImage) throws IOException {
        log.info("image store folder is " + path);
        Resource resource = resourceLoader.getResource("classpath:static/image/");
        File folder = new File(resource.getFile().getAbsolutePath() + File.separator + path + (isBigImage ? "/bigimage/" : "/sample/"));

        if (!checkImageFolderIsExists(folder.getAbsolutePath())) {
            log.info("image store folder " + folder.getAbsolutePath() + " not exists");
            folder.mkdirs();
            log.info("image store folder " + folder.getAbsolutePath() + " created");
        } else {
            log.info("image store folder " + folder.getAbsolutePath() + " exists");
        }

        if (checkImageIsExists(folder.getAbsolutePath() + File.separator + fileName, fileName)) {
            log.info("image " + folder.getAbsolutePath() + File.separator + fileName + " exists");
            return;
        }

        try (FileOutputStream fos = new FileOutputStream(new File(folder.getAbsolutePath() + File.separator + fileName))) {
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
