# 查找所有 scrapy 进程并杀死它们
pgrep -f "scrapy crawl" | xargs -r kill
echo "查找并杀死所有scrapy进程..."