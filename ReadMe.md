<!--
 * @Date: 2025-02-09 18:57:08
 * @LastEditors: MajorTomMan 765719516@qq.com
 * @LastEditTime: 2025-02-13 22:15:00
 * @FilePath: \spider\ReadMe.md
 * @Description: MajorTomMan @版权声明 保留文件所有权利
-->
运行爬虫命令

先启动movie和actress_detail爬虫作为消费者

scrapy crawl movie

scrapy crawl actress_detail

scrapy crawl actress_movie

首页:

scrapy crawl index -a url=https://www.javbus.com/page/ -a is_censored=True

scrapy crawl index -a url=https://www.javbus.com/uncensored/page/ -a is_censored=True

搜索:

scrapy crawl search -a actress="北野未奈"

scrapy crawl search -a code="OFJE-459"

scrapy crawl search -a director="麒麟"

......

女优列表页:

scrapy crawl actresses_list -a is_censored = False

类别页:

scrapy crawl genre -a is_censored = False
