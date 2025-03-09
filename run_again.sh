
# 启动首页爬虫并记录日志
nohup scrapy crawl index -a is_censored=True > ~/logs/index_censored.log 2>&1 &
PID_index_censored=$!
echo "Index Censored spider is running with PID: $PID_index_censored"

nohup scrapy crawl index -a is_censored=False > ~/logs/index_uncensored.log 2>&1 &
PID_index_uncensored=$!
echo "Index Uncensored spider is running with PID: $PID_index_uncensored"