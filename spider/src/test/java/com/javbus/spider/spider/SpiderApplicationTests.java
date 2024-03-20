package com.javbus.spider.spider;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.javbus.spider.spider.utils.EmailUtil;

@SpringBootTest
class SpiderApplicationTests {
	@Autowired
	private EmailUtil util;
	@Test
	void testMail() {
		util.sendEmail("测试", "测试");
	}

}
