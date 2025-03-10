#!/bin/bash

# 获取当前脚本所在目录
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

echo "脚本目录: $SCRIPT_DIR"

# 进入脚本所在目录
cd "$SCRIPT_DIR" || { echo "无法进入脚本目录: $SCRIPT_DIR"; exit 1; }

# 查找所有 scrapy 进程并杀死它们
 pgrep -f "scrapy crawl" | xargs -r kill
 echo "查找并杀死所有scrapy进程..."
 
 # 检查是否安装了 cron
 if ! command -v cron &> /dev/null
 then
     echo "cron 未安装，正在安装 cron..."
     sudo apt update
     sudo apt install cron -y
 else
     echo "cron 已安装"
 fi
# 启动 cron 服务
 sudo service cron start

 # 确认 cron 服务是否正在运行
 if systemctl is-active --quiet cron
 then
     echo "cron 服务正在运行"
 else
     echo "cron 服务启动失败"
 fi
 # 检查是否安装了 Python3
 if ! command -v python3 &> /dev/null
 then
     echo "Python3 未安装，请先安装 Python3!"
     exit 1
 fi

 # 检查是否安装了 venv 模块
 if ! python3 -m venv --help &> /dev/null
 then
     echo "未安装 python3-venv 模块，正在安装..."
     sudo apt install python3-venv -y
 fi

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
      "$SCRIPT_DIR/logs/genre_censored.log" "$SCRIPT_DIR/logs/genre_uncensored.log" "$SCRIPT_DIR/logs/pids.log" \
      "$SCRIPT_DIR/logs/index_again.log "

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
> "$SCRIPT_DIR/logs/index_again.log"

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

# 第一批爬虫的 kill 命令
 kill_command_first_batch=$(echo "$PID_index_censored $PID_index_uncensored $PID_actresses_list_censored $PID_actresses_list_uncensored $PID_genre_censored $PID_genre_uncensored" | xargs -I {} echo "kill -9 {}")
 
 # 输出第一批的 kill 命令
 echo "以下是可以用来终止第一批爬虫进程的命令："
 echo "$kill_command_first_batch"
 
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


# 第二批爬虫的 kill 命令
kill_command_second_batch=$(echo "$PID_movie $PID_actress_movie $PID_actress_detail" | xargs -I {} echo "kill -9 {}")
# 输出第二批的 kill 命令
 echo "以下是可以用来终止第二批爬虫进程的命令："
 echo "$kill_command_second_batch"


 
# 添加定时任务 (cron) 每三天执行一次 index_censored 和 index_uncensored 爬虫
(crontab -l ; echo "0 0 */3 * * /bin/bash $SCRIPT_DIR/run_spiders.sh > $SCRIPT_DIR/logs/index_again.log ") | crontab -

echo "已添加定时任务：每三天执行一次爬虫"
