import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from base import model_one
from proxy_pool import ProxyPool


def timed_task(loop, proxy):
    loop.run_until_complete(model_one(loop, proxy, 1))


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    proxy = ProxyPool()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=timed_task, args=(event_loop, proxy), trigger='interval', seconds=10)
    scheduler.start()
    try:
        event_loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
