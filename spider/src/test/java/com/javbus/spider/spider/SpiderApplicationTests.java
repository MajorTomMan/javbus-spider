/*
 * @Date: 2024-04-24 20:38:19
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2024-04-24 20:45:04
 * @FilePath: \Python\JavBus\spider\src\test\java\com\javbus\spider\spider\SpiderApplicationTests.java
 * @Description: MajorTomMan @版权声明 保留文件所有权利
 */
package com.javbus.spider.spider;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.utils.EmailUtil;
import com.javbus.spider.spider.utils.ImageUtil;

import lombok.extern.log4j.Log4j2;

@Log4j2
@SpringBootTest
class SpiderApplicationTests {
	@Autowired
	private EmailUtil util;
	@Autowired
	private ActressDao actressDao;
	@Autowired
	private ImageUtil imageUtil;
	@Test
	void testMail() {
		util.sendEmail("测试", "测试");
	}
	@Test
	void testImage(){
	}
}
