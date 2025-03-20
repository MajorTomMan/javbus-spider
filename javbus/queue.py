'''
Date: 2025-03-10 21:19:43
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-03-19 23:58:02
FilePath: \spider\javbus\queue.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
from scrapy_redis.queue import Base
import time
from scrapy_redis.dupefilter import RFPDupeFilter  # 引入去重过滤器

# 根据scrapy_redis源码参考
# 实现的一个根据时间戳递增保证有序且先进后出的集合结构
# 尽量保证高并发时能做到唯一
class LifoSortedQueue(Base):
    """Per-spider FIFO queue"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.zcard(self.key)

    def push(self, request):
        """Push a request"""
        data = self._encode_request(request=request)
        # 获取微秒级别的时间戳
        timestamp_us = int(time.time() * 1_000_000)
        counter_id = self.server.incr("unique_id")
        score = timestamp_us + counter_id
        self.server.execute_command("ZADD", self.key, score, data)

    def pop(self, timeout=0):
        """Pop a request"""

        # use atomic range/remove using multi/exec
        pipe = self.server.pipeline()
        pipe.multi()
        # 取出分数最大的元素（后进先出）
        # 取出并从redis中删除最新的数据
        pipe.zrange(self.key, -1, -1)  
        pipe.zremrangebyrank(self.key, -1, -1)
        results, count = pipe.execute()
        if results:
            return self._decode_request(results[0])


# 根据scrapy_redis源码参考
# 实现的一个根据时间戳递增保证有序且先进先出的集合结构
# 尽量保证高并发时能做到唯一
class FifoSortedQueue(Base):
    """Per-spider FIFO queue"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.zcard(self.key)

    def push(self, request):
        """Push a request"""
        data = self._encode_request(request=request)
        # 获取微秒级别的时间戳
        timestamp_us = int(time.time() * 1_000_000)
        counter_id = self.server.incr("unique_id")
        score = timestamp_us + counter_id
        self.server.execute_command("ZADD", self.key, score, data)

    def pop(self, timeout=0):
        """Pop a request"""

        # use atomic range/remove using multi/exec
        pipe = self.server.pipeline()
        pipe.multi()
        # 取出时间最前面的元素（先进先出）
        # 取出并从redis中删除最旧的数据
        pipe.zrange(self.key, 0, 0)
        pipe.zremrangebyrank(self.key, 0, 0)
        results, count = pipe.execute()
        if results:
            request = self._decode_request(results[0])
            # 先验证是否是请求过的,做增量更新
            if self.spider.crawler.engine.slot.scheduler.df.request_seen(request):
                return None
            return request
