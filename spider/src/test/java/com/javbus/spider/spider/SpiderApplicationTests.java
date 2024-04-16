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
		List<Integer> of = List.of(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
		List<Actress> queryActresses = actressDao.queryActressesById(of);
		queryActresses.forEach(a->{
			log.info(a);
		});
		byte[] bytes={0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};
		imageUtil.saveBigImage(bytes,queryActresses,"114514","test.jpg");
	}
}
