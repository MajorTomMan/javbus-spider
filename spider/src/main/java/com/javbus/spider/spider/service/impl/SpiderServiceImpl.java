package com.javbus.spider.spider.service.impl;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponents;
import org.springframework.web.util.UriComponentsBuilder;
import com.javbus.spider.spider.dao.SpiderDao;
import com.javbus.spider.spider.entity.ApiResponse;
import com.javbus.spider.spider.entity.Question;
import com.javbus.spider.spider.entity.QuestionData;
import com.javbus.spider.spider.service.SpiderService;

import lombok.extern.log4j.Log4j2;
@Service("spiderSerivce")
@Log4j2
public class SpiderServiceImpl implements SpiderService {
    private int pageNum = 1;
    private int type = 1;
    private String App_id = "ptlgislxnloi2wxs";
    private String App_Secret = "hQqWr0Z9lZehJZ8F19c0qcaZNUcAGd9E";
    private String url = "https://www.mxnzp.com/api/driver_exam/question/list";
    @Autowired
    private SpiderDao spiderDao;
    @Autowired
    private RestTemplate template;

    @Override
    public String getAnswer(String title) {
        // TODO Auto-generated method stub
        Question question = spiderDao.getQuestionByTitle(title);
        if (question != null) {
            return question.getOp1();
        }
        return null;
    }

    @Override
    public void updateQuestion() throws URISyntaxException {
        // TODO Auto-generated method stub
        URI uri = new URI(url);
        UriComponents uriComponents = UriComponentsBuilder.fromUri(uri)
                .queryParam("page", pageNum)
                .queryParam("rank", 1)
                .queryParam("type", type)
                .queryParam("app_id", App_id)
                .queryParam("app_secret", App_Secret)
                .build();
        String fullUrl = uriComponents.toUriString();
        if (StringUtils.hasText(fullUrl)) {
            ResponseEntity<ApiResponse<QuestionData>> response = template.exchange(
                    fullUrl,
                    HttpMethod.GET,
                    null,
                    new ParameterizedTypeReference<ApiResponse<QuestionData>>() {
                    });
            HttpStatusCode statusCode = response.getStatusCode();
            if (statusCode.is2xxSuccessful()) {
                ApiResponse<QuestionData> body = response.getBody();
                QuestionData data = body.getData();
                List<Question> questions = data.getQuestions();
                for (Question question : questions) {
                    log.info("title:" + question.getTitle());
                    log.info("option 1:" + question.getOp1());
                    log.info("option 2:" + question.getOp2());
                    log.info("option 3:" + question.getOp3());
                    log.info("option 4:" + question.getOp4());
                    spiderDao.insertQuestion(question);
                }
            }
        } else {
            log.info("path is null or empty");
        }
    }
}
