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

import com.javbus.spider.spider.entity.dto.BigImageDTO;
import com.javbus.spider.spider.entity.dto.SampleImageDTO;

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

    public void saveBigImage(BigImageDTO image) {
        String imagePath = imageFolder + image.getName() + File.separator + image.getCode() + File.separator
                + "bigimage"
                + File.separator;
        save(image.getBigImage(), imagePath, image.getFileName());
    }

    public void saveBigImage(List<BigImageDTO> images) {
        for (BigImageDTO dto : images) {
            String imagePath = imageFolder + dto.getName() + File.separator + dto.getCode() + File.separator
                    + "bigimage"
                    + File.separator;
            save(dto.getBigImage(), imagePath, dto.getFileName());
        }
    }

    public void saveSampleImage(SampleImageDTO image) {
        String imagePath = imageFolder + image.getName() + File.separator + image.getCode() + File.separator + "sample"
                + File.separator;
        save(image.getSampleImage(), imagePath, image.getFileName());
    }

    public void saveSampleImage(List<SampleImageDTO> images) {
        for (SampleImageDTO dto : images) {
            String imagePath = imageFolder + dto.getName() + File.separator + dto.getCode() + File.separator
                    + "sample"
                    + File.separator;
            save(dto.getSampleImage(), imagePath, dto.getFileName());
        }
    }

    private void save(byte[] image, String path, String fileName) {
        log.info("image store folder is " + path);
        File folder = new File(path);
        if (!folder.exists()) {
            log.info("image store folder " + path + " not exists");
            folder.mkdirs();
            log.info("image store folder " + path + " created");
        } else {
            log.info("image store folder " + path + " exists");
        }
        try (FileOutputStream fos = new FileOutputStream(new File(path + fileName))) {
            fos.write(image);
            log.info("image " + fileName + " downloaded");
            log.info("image store path is " + path + fileName);
        } catch (IOException e) {
            log.error("image " + fileName + " download failed");
            log.error("reason:" + e.getMessage());
        }
    }

    public boolean checkImageIsExists(BigImageDTO dto) {
        String imagePath = imageFolder + dto.getName() + File.separator + dto.getCode() + File.separator
                + "bigimage"
                + File.separator + dto.getFileName();
        File file = new File(imagePath);
        if (file.exists()) {
            log.info("image " + imagePath + " was exists");
            return true;
        }
        return false;
    }

    public boolean checkImageIsExists(SampleImageDTO dto) {
        String imagePath = imageFolder + dto.getName() + File.separator + dto.getCode() + File.separator
                + "sample"
                + File.separator + dto.getFileName();
        File file = new File(imagePath);
        if (file.exists()) {
            log.info("image " + imagePath + " was exists");
            return true;
        }
        return false;
    }
}
