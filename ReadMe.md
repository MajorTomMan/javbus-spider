<!--
 * @Date: 2025-02-09 18:57:08
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2025-02-09 18:59:25
 * @FilePath: \spider\ReadMe.md
 * @Description: MajorTomMan @版权声明 保留文件所有权利
-->
运行爬虫命令

先启动movie和actress_detail爬虫作为消费者

scrapy crawl movie

scrapy crawl actress_detail

首页:

scrapy crawl index -a url=https://www.javbus.com/page/ -a is_censored=True

scrapy crawl index -a url=https://www.javbus.com/uncensored/page/ -a is_censored=True

搜索:

女优列表页:

类别页:
