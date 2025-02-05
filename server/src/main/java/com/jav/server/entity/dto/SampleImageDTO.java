package com.jav.server.entity.dto;

import lombok.Data;

@Data
public class SampleImageDTO {
    private String name;
    private String code;
    private String fileName;
    private byte[] sampleImage;
}
