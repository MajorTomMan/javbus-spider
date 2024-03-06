package com.javbus.spider.spider.service;

import java.net.URISyntaxException;

import org.springframework.stereotype.Service;

@Service
public interface SpiderService {
    public String getAnswer(String title);
    public void updateQuestion() throws URISyntaxException;
}
