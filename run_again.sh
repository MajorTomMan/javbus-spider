
# 获取当前脚本所在目录
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
# 进入脚本所在目录
cd "$SCRIPT_DIR" || { echo "无法进入脚本目录: $SCRIPT_DIR"; exit 1; }



# 启动首页爬虫并记录日志
nohup scrapy crawl index -a is_censored=True > "$SCRIPT_DIR/logs/index_censored.log" 2>&1 &
PID_index_censored=$!
echo "Index Censored spider is running with PID: $PID_index_censored"

nohup scrapy crawl index -a is_censored=False > "$SCRIPT_DIR/logs/index_uncensored.log" 2>&1 &
PID_index_uncensored=$!
echo "Index Uncensored spider is running with PID: $PID_index_uncensored"

kill_command_batch=$(echo "$PID_index_censored $PID_index_uncensored" | xargs -I {} echo "kill -9 {}")


 # kill 命令
 echo "以下是可以用来终止第一批爬虫进程的命令："
 echo "$kill_command_batch"