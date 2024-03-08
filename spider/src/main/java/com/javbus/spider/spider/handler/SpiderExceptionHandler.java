package com.javbus.spider.spider.handler;

import java.net.ConnectException;
import java.sql.SQLIntegrityConstraintViolationException;

import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import com.javbus.spider.spider.utils.R;

import lombok.extern.log4j.Log4j2;

@Log4j2
@ControllerAdvice
public class SpiderExceptionHandler {
    @ExceptionHandler(SQLIntegrityConstraintViolationException.class)
    public R handleException(SQLIntegrityConstraintViolationException e) {
        log.error("主键重复");
        log.error(e.getMessage());
        log.error(e.getClass());
        return R.ok();
    }
    @ExceptionHandler(ConnectException.class)
    public R handleException(ConnectException e){
        log.error(e.getMessage());
        log.error(e.getClass());
        return R.error();
    }
}
