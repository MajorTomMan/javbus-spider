:: 启动 movie 和 actress_detail 爬虫作为消费者
start cmd /K "title Movie && scrapy crawl movie"
start cmd /K "title Actress Detail && scrapy crawl actress_detail"
start cmd /K "title Actress Movie && scrapy crawl actress_movie"

:: 启动首页爬虫
start cmd /K "title Index - Censored && scrapy crawl index -a is_censored=True"
start cmd /K "title Index - Uncensored && scrapy crawl index -a is_censored=False"

:: 启动女优列表页爬虫
start cmd /K "title Actresses List - Censored && scrapy crawl actresses_list -a is_censored=True"
start cmd /K "title Actresses List - Uncensored && scrapy crawl actresses_list -a is_censored=False"

:: 启动类别页爬虫
start cmd /K "title Genre - Censored && scrapy crawl genre -a is_censored=True"
start cmd /K "title Genre - Uncensored && scrapy crawl genre -a is_censored=False"
