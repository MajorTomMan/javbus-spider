
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

    public void saveImages(List<byte[]> images, List<String> actresses, String code, List<String> fileNames,Boolean isBigImage) {
        for (int i=0;i<images.size();i++) {
            try {
                save(images.get(i), actresses, code, fileNames.get(i), isBigImage);
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    private void save(byte[] image, List<String> actresses, String code, String fileName, Boolean isBigImage)
            throws IOException {
        Resource resource = resourceLoader.getResource("classpath:static/image/");
        File file = new File(resource.getFile().getAbsolutePath());
        save(file.getAbsolutePath(), actresses, code, isBigImage, fileName, image);
    }

    private void save(String path, List<String> names, String code, boolean isBigImage, String fileName, byte[] image) {
        String root = path;
        saveRecursive(root, names, code, fileName, isBigImage, image);
    }

    private void saveRecursive(String root, List<String> names, String code, String fileName, boolean isBigImage,
            byte[] image) {
        if (names.isEmpty()) {
            return;
        }

        // 获取当前人名
        String currentName = names.get(0);

        // 构建当前文件夹路径
        String currentFolderPath = root + File.separator + currentName;

        // 递归创建子文件夹
        saveRecursive(currentFolderPath, names.subList(1, names.size()), code, fileName, isBigImage, image);

        // 如果是最后一个人名，执行创建和写入操作
        if (names.size() == 1) {
            try {
                currentFolderPath += File.separator + code;
                save(image, currentFolderPath, fileName, isBigImage);
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    private void save(byte[] image, String path, String fileName, Boolean isBigImage) throws IOException {
        log.info("image store folder is " + path);
        File folder = new File(path + (isBigImage ? "/bigimage/" : "/sample/"));
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
        File file = new File(folder.getAbsolutePath() + File.separator + fileName);
        try (FileOutputStream fos = new FileOutputStream(file)) {
            fos.write(image);
            log.info("image " + fileName + " downloaded");
            log.info("image store path is " + file.getAbsolutePath());
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
