@echo off

:: 创建 logs 目录（如果不存在）
if not exist logs (
    mkdir logs
)

:: 启动 movie 和 actress_detail 爬虫作为消费者并保存日志到文件
start /B cmd /C "scrapy crawl movie > logs/movie.log 2>&1"
set MOVIE_PID=%ERRORLEVEL%
echo Movie spider is running with PID %MOVIE_PID% and logging to logs/movie.log

start /B cmd /C "scrapy crawl actress_detail > logs/actress_detail.log 2>&1"
set ACTRESS_DETAIL_PID=%ERRORLEVEL%
echo Actress Detail spider is running with PID %ACTRESS_DETAIL_PID% and logging to logs/actress_detail.log

start /B cmd /C "scrapy crawl actress_movie > logs/actress_movie.log 2>&1"
set ACTRESS_MOVIE_PID=%ERRORLEVEL%
echo Actress Movie spider is running with PID %ACTRESS_MOVIE_PID% and logging to logs/actress_movie.log

:: 启动首页爬虫
start /B cmd /C "scrapy crawl index -a is_censored=True > logs/index_censored.log 2>&1"
set INDEX_CENSORED_PID=%ERRORLEVEL%
echo Index Censored spider is running with PID %INDEX_CENSORED_PID% and logging to logs/index_censored.log

start /B cmd /C "scrapy crawl index -a is_censored=False > logs/index_uncensored.log 2>&1"
set INDEX_UNCENSORED_PID=%ERRORLEVEL%
echo Index Uncensored spider is running with PID %INDEX_UNCENSORED_PID% and logging to logs/index_uncensored.log

:: 启动女优列表页爬虫
start /B cmd /C "scrapy crawl actresses_list -a is_censored=True > logs/actresses_list_censored.log 2>&1"
set ACTRESSES_LIST_CENSORED_PID=%ERRORLEVEL%
echo Actresses List Censored spider is running with PID %ACTRESSES_LIST_CENSORED_PID% and logging to logs/actresses_list_censored.log

start /B cmd /C "scrapy crawl actresses_list -a is_censored=False > logs/actresses_list_uncensored.log 2>&1"
set ACTRESSES_LIST_UNCENSORED_PID=%ERRORLEVEL%
echo Actresses List Uncensored spider is running with PID %ACTRESSES_LIST_UNCENSORED_PID% and logging to logs/actresses_list_uncensored.log

:: 启动类别页爬虫
start /B cmd /C "scrapy crawl genre -a is_censored=True > logs/genre_censored.log 2>&1"
set GENRE_CENSORED_PID=%ERRORLEVEL%
echo Genre Censored spider is running with PID %GENRE_CENSORED_PID% and logging to logs/genre_censored.log

start /B cmd /C "scrapy crawl genre -a is_censored=False > logs/genre_uncensored.log 2>&1"
set GENRE_UNCENSORED_PID=%ERRORLEVEL%
echo Genre Uncensored spider is running with PID %GENRE_UNCENSORED_PID% and logging to logs/genre_uncensored.log

:: 输出所有爬虫的进程PID
echo "所有爬虫的进程号："
echo Movie spider PID: %MOVIE_PID%
echo Actress Detail spider PID: %ACTRESS_DETAIL_PID%
echo Actress Movie spider PID: %ACTRESS_MOVIE_PID%
echo Index Censored spider PID: %INDEX_CENSORED_PID%
echo Index Uncensored spider PID: %INDEX_UNCENSORED_PID%
echo Actresses List Censored spider PID: %ACTRESSES_LIST_CENSORED_PID%
echo Actresses List Uncensored spider PID: %ACTRESSES_LIST_UNCENSORED_PID%
echo Genre Censored spider PID: %GENRE_CENSORED_PID%
echo Genre Uncensored spider PID: %GENRE_UNCENSORED_PID%

:: 一行显示所有的 taskkill 命令
echo "以下是可以用来杀死所有爬虫进程的命令："
echo taskkill /PID %MOVIE_PID% /F & taskkill /PID %ACTRESS_DETAIL_PID% /F & taskkill /PID %ACTRESS_MOVIE_PID% /F & taskkill /PID %INDEX_CENSORED_PID% /F & taskkill /PID %INDEX_UNCENSORED_PID% /F & taskkill /PID %ACTRESSES_LIST_CENSORED_PID% /F & taskkill /PID %ACTRESSES_LIST_UNCENSORED_PID% /F & taskkill /PID %GENRE_CENSORED_PID% /F & taskkill /PID %GENRE_UNCENSORED_PID% /F

echo "所有爬虫已在后台运行，日志保存在 logs 目录下"
