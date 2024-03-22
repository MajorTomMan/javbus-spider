package com.javbus.spider.spider;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

@SpringBootApplication
public class SpiderApplication extends SpringBootServletInitializer{

	public static void main(String[] args) {
		SpringApplication.run(SpiderApplication.class, args);
	}
	    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application){
        //指定 @SpringBootApplication 所在类
        return application.sources(SpiderApplication.class);
    }
}
