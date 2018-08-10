import time
from motor import motor_asyncio


class StoreInfo:

    def __init__(self, config):
        self.db = motor_asyncio.AsyncIOMotorClient(config['host'], config['port'])['douban']
        self.year = time.strftime('%Y', time.localtime(time.time()))

    def get_timestamp(self, ftime):
        if len(ftime) == 11:
            ts = time.strptime(self.year + "-" + ftime, "%Y-%m-%d %H:%M")
        else:
            ts = time.strptime(ftime, "%Y-%m-%d %H:%M")
        return time.mktime(ts)

    async def store_info(self, info):
        info['timestamp'] = self.get_timestamp(info['recent'])
        await self.db.discussion.insert_one(info)

    async def update_info(self, topic_id, comment_num, recent):
        timestamp = self.get_timestamp(recent)
        await self.db.discussion.update_one({'topic_id': topic_id}, {'$set': {
            'recent': recent,
            'comment_num': comment_num,
            'timestamp': timestamp
        }})
