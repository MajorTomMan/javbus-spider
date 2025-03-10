#!/bin/bash

# 获取当前脚本所在目录
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

echo "脚本目录: $SCRIPT_DIR"

# 进入脚本所在目录
cd "$SCRIPT_DIR" || { echo "无法进入脚本目录: $SCRIPT_DIR"; exit 1; }

# 其他操作...

# 创建虚拟环境目录
VENV_DIR="$SCRIPT_DIR/myvenv"
if [ ! -d "$VENV_DIR" ]; then
    echo "创建虚拟环境 $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
else
    echo "虚拟环境 $VENV_DIR 已存在，跳过创建步骤."
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 安装项目依赖
echo "安装项目依赖..."
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"

# 创建日志目录
mkdir -p "$SCRIPT_DIR/logs"

# 创建日志文件（如果不存在）
touch "$SCRIPT_DIR/logs/movie.log" "$SCRIPT_DIR/logs/actress_detail.log" "$SCRIPT_DIR/logs/actress_movie.log" \
      "$SCRIPT_DIR/logs/index_censored.log" "$SCRIPT_DIR/logs/index_uncensored.log" \
      "$SCRIPT_DIR/logs/actresses_list_censored.log" "$SCRIPT_DIR/logs/actresses_list_uncensored.log" \
      "$SCRIPT_DIR/logs/genre_censored.log" "$SCRIPT_DIR/logs/genre_uncensored.log" "$SCRIPT_DIR/logs/pids.log"

# 清空日志文件
> "$SCRIPT_DIR/logs/movie.log"
> "$SCRIPT_DIR/logs/actress_detail.log"
> "$SCRIPT_DIR/logs/actress_movie.log"
> "$SCRIPT_DIR/logs/index_censored.log"
> "$SCRIPT_DIR/logs/index_uncensored.log"
> "$SCRIPT_DIR/logs/actresses_list_censored.log"
> "$SCRIPT_DIR/logs/actresses_list_uncensored.log"
> "$SCRIPT_DIR/logs/genre_censored.log"
> "$SCRIPT_DIR/logs/genre_uncensored.log"
> "$SCRIPT_DIR/logs/pids.log"

# 启动第一批爬虫并记录日志
nohup scrapy crawl index -a is_censored=True > "$SCRIPT_DIR/logs/index_censored.log" 2>&1 &
PID_index_censored=$!
echo "Index Censored spider is running with PID: $PID_index_censored"

nohup scrapy crawl index -a is_censored=False > "$SCRIPT_DIR/logs/index_uncensored.log" 2>&1 &
PID_index_uncensored=$!
echo "Index Uncensored spider is running with PID: $PID_index_uncensored"

nohup scrapy crawl actresses_list -a is_censored=True > "$SCRIPT_DIR/logs/actresses_list_censored.log" 2>&1 &
PID_actresses_list_censored=$!
echo "Actresses List Censored spider is running with PID: $PID_actresses_list_censored"

nohup scrapy crawl actresses_list -a is_censored=False > "$SCRIPT_DIR/logs/actresses_list_uncensored.log" 2>&1 &
PID_actresses_list_uncensored=$!
echo "Actresses List Uncensored spider is running with PID: $PID_actresses_list_uncensored"

nohup scrapy crawl genre -a is_censored=True > "$SCRIPT_DIR/logs/genre_censored.log" 2>&1 &
PID_genre_censored=$!
echo "Genre Censored spider is running with PID: $PID_genre_censored"

nohup scrapy crawl genre -a is_censored=False > "$SCRIPT_DIR/logs/genre_uncensored.log" 2>&1 &
PID_genre_uncensored=$!
echo "Genre Uncensored spider is running with PID: $PID_genre_uncensored"

# 等待所有爬虫结束
wait_for_scrapy_to_finish() {
    echo "等待当前 Scrapy 爬虫完成..."
    while true; do
        running_pids=$(pgrep -f "scrapy crawl")
        if [ -z "$running_pids" ]; then
            echo "所有爬虫都已经完成，启动 movie, actress_movie 和 actress_detail ..."
            break
        else
            sleep 5  # 每隔 5 秒检查一次
        fi
    done
}

# 启动第二批爬虫
start_remaining_spiders() {
    nohup scrapy crawl movie > "$SCRIPT_DIR/logs/movie.log" 2>&1 &
    PID_movie=$!
    echo "Movie spider is running with PID: $PID_movie"

    nohup scrapy crawl actress_movie > "$SCRIPT_DIR/logs/actress_movie.log" 2>&1 &
    PID_actress_movie=$!
    echo "Actress Movie spider is running with PID: $PID_actress_movie"

    nohup scrapy crawl actress_detail > "$SCRIPT_DIR/logs/actress_detail.log" 2>&1 &
    PID_actress_detail=$!
    echo "Actress Detail spider is running with PID: $PID_actress_detail"
}

# 执行监控并启动剩余爬虫
wait_for_scrapy_to_finish
start_remaining_spiders

# 添加定时任务 (cron) 每三天执行一次 index_censored 和 index_uncensored 爬虫
(crontab -l ; echo "0 0 */3 * * /bin/bash $SCRIPT_DIR/run_spiders.sh") | crontab -

echo "已添加定时任务：每三天执行一次爬虫"
