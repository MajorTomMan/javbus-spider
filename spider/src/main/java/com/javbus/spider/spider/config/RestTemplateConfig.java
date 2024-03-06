package com.javbus.spider.spider.config;

import java.time.Duration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.ClientHttpRequestFactory;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

/**
 * RestTemplateConfig
 */
@Configuration
public class RestTemplateConfig {
    @Bean
    public RestTemplate restTemplate(ClientHttpRequestFactory factory){
        return new RestTemplate();
    }
    @Bean
    public ClientHttpRequestFactory configureClientHttpRequestFactory(){
        SimpleClientHttpRequestFactory clientHttpRequestFactory=new SimpleClientHttpRequestFactory();
        clientHttpRequestFactory.setReadTimeout(Duration.ofMinutes(10));
        clientHttpRequestFactory.setConnectTimeout(Duration.ofMinutes(10));
        return clientHttpRequestFactory;
    }
}