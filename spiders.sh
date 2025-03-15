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
#mkdir -p "$SCRIPT_DIR/outputs"
# 创建日志文件（如果不存在）
touch "$SCRIPT_DIR/logs/movie.log" "$SCRIPT_DIR/logs/actress_detail.log" "$SCRIPT_DIR/logs/actress_movie.log" \
      "$SCRIPT_DIR/logs/genre_censored.log" "$SCRIPT_DIR/logs/genre_uncensored.log" \

# 清空日志文件
> "$SCRIPT_DIR/logs/movie.log"
> "$SCRIPT_DIR/logs/actress_detail.log"
> "$SCRIPT_DIR/logs/actress_movie.log"
> "$SCRIPT_DIR/logs/genre_censored.log"
> "$SCRIPT_DIR/logs/genre_uncensored.log"

nohup scrapy crawl index -a is_censored=True > "$SCRIPT_DIR/logs/index_censored.log" 2>&1 &
PID_index_censored=$!
echo "Index Censored spider is running with PID: $PID_index_censored"

nohup scrapy crawl index -a is_censored=False > "$SCRIPT_DIR/logs/index_uncensored.log" 2>&1 &
PID_index_uncensored=$!
echo "Index Uncensored spider is running with PID: $PID_index_uncensored"

nohup scrapy crawl actresses_list -a is_censored=True > $SCRIPT_DIR/logs/actresses_list_true.log  2>&1 &
PID_actresses_list_true=$!
nohup scrapy crawl actresses_list -a is_censored=False > $SCRIPT_DIR/logs/actresses_list_false.log 2>&1 &
PID_actresses_list_false=$!
#nohup scrapy crawl movie > "$SCRIPT_DIR/logs/movie.log" 2>&1 &
#PID_movie=$!
#echo "Movie spider is running with PID: $PID_movie"

#nohup scrapy crawl actress_movie > "$SCRIPT_DIR/logs/actress_movie.log" 2>&1 &
#PID_actress_movie=$!
#echo "Actress Movie spider is running with PID: $PID_actress_movie"

#nohup scrapy crawl actress_detail > "$SCRIPT_DIR/logs/actress_detail.log" 2>&1 &
#PID_actress_detail=$!
#echo "Actress Detail spider is running with PID: $PID_actress_detail"

nohup scrapy crawl genre -a is_censored=True > "$SCRIPT_DIR/logs/genre_censored.log" 2>&1 &
PID_genre_censored=$!
echo "Genre Censored spider is running with PID: $PID_genre_censored"

nohup scrapy crawl genre -a is_censored=False > "$SCRIPT_DIR/logs/genre_uncensored.log" 2>&1 &
PID_genre_uncensored=$!
echo "Genre Uncensored spider is running with PID: $PID_genre_uncensored"

kill_command_first_batch=$(echo "$PID_index_censored $PID_index_uncensored $PID_actresses_list_censored $PID_actresses_list_uncensored $PID_genre_censored $PID_genre_uncensored" | xargs -I {} echo "kill -9 {}")
#kill_command_batch=$(echo "$PID_actresses_list_true $PID_actresses_list_false | xargs -I {} echo "kill -9 {}")
 
echo "以下是可以用来爬虫进程的命令："
echo "$kill_command_batch"