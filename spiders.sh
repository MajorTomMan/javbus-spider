#!/bin/bash
###
 # @Date: 2025-02-14 20:07:34
 # @LastEditors: MajorTomMan 765719516@qq.com
 # @LastEditTime: 2025-02-16 19:18:08
 # @FilePath: \spider\spiders.sh
 # @Description: MajorTomMan @版权声明 保留文件所有权利
### 

sudo apt-get install tmux

# 启动 tmux 会话
tmux new-session -s spiders:movie 'scrapy crawl movie' # 会话1: movie
tmux new-window -t spiders:actress_detail 'scrapy crawl actress_detail' # 会话2: actress_detail
tmux new-window -t spiders:actress_movie 'scrapy crawl actress_movie' # 会话3: actress_movie

# 启动首页爬虫
tmux new-window -t spiders:index_censored 'scrapy crawl index -a url=https://www.javbus.com/page/ -a is_censored=True' # 会话4: index censored
tmux new-window -t spiders:index_uncensored 'scrapy crawl index -a url=https://www.javbus.com/uncensored/page/ -a is_censored=False' # 会话5: index uncensored


# 启动女优列表页爬虫
tmux new-window -t spiders:actresses_list_censored 'scrapy crawl actresses_list -a is_censored=True' # 会话9: actresses_list censored
tmux new-window -t spiders:actresses_list_uncensored 'scrapy crawl actresses_list -a is_censored=False' # 会话10: actresses_list uncensored

# 启动类别页爬虫
tmux new-window -t spiders:genre_censored 'scrapy crawl genre -a is_censored=True' # 会话11: genre censored
tmux new-window -t spiders:genre_uncensored 'scrapy crawl genre -a is_censored=False' # 会话12: genre uncensored

# 附加到 tmux 会话
tmux attach-session -t spiders