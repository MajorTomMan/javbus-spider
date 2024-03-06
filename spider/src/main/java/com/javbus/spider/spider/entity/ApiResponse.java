package com.javbus.spider.spider.entity;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

import java.util.List;

@Data
public class ApiResponse<T> {

    private int code;

    private String msg;

    private T data;

    // Getter and Setter methods
}