package com.javbus.spider.spider.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.service.SpiderService;

import java.net.URISyntaxException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;


@RestController
@RequestMapping("driver")
public class SpiderController {
    @Autowired
    private SpiderService service;
    @PostMapping("/question")
    public String getQuestion(@RequestParam("title") String title){
        String answer = service.getAnswer(title);
        if(answer!=null){
            return null; 
        }
        return answer;
    }
    @GetMapping("/update")
    public void updateQuestion() throws URISyntaxException{
        service.updateQuestion();
    }
}
