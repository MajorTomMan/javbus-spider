:: 启动 movie 和 actress_detail 爬虫作为消费者
start cmd /K "scrapy crawl movie"
start cmd /K "scrapy crawl actress_detail"
start cmd /K "scrapy crawl actress_movie"

:: 启动首页爬虫
start cmd /K "scrapy crawl index -a url=https://www.javbus.com/page/ -a is_censored=True"
start cmd /K "scrapy crawl index -a url=https://www.javbus.com/uncensored/page/ -a is_censored=False"

:: 启动女优列表页爬虫
start cmd /K "scrapy crawl actresses_list -a is_censored=True"
start cmd /K "scrapy crawl actresses_list -a is_censored=False"

:: 启动类别页爬虫
start cmd /K "scrapy crawl genre -a is_censored=True"
start cmd /K "scrapy crawl genre -a is_censored=False"