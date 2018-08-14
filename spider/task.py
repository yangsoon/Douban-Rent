import time
import asyncio
from base import model_one
from proxy_pool import ProxyPool

import logging
from util import log
from config import wait_time

log(logging, None)

if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    logging.info("定时任务开始")
    while True:
        start = time.time()
        proxy = ProxyPool()
        event_loop.run_until_complete(model_one(event_loop, proxy, 5))
        waste = (time.time() - start) / 60
        logging.info(f"此处任务耗时{round(waste, 2)}分钟")
        logging.info("waitting....")
        time.sleep(wait_time)


