from scrapy.cmdline import execute

def run_spider():
    # 模拟命令行执行 scrapy crawl 命令
    execute(['scrapy', 'crawl', 'javbus.spiders'])

if __name__ == '__main__':
    run_spider()
