from venv import logger
from motor.motor_asyncio import AsyncIOMotorClient
from db_conf import mongodb_conf


class YaMongoPool(AsyncIOMotorClient):

    def __init__(self, conf):
        super().__init__(**conf)
        logger.info('YaMongoPool gets ready')


mongodb_pool = YaMongoPool(conf=mongodb_conf)


class Mongo:
    def __init__(self, mongo_pool):
        self.db = mongo_pool

    async def replace_one(self, database, table_name, value):
        return await self.db[database][table_name].replace_one(filter={'uuid': value['uuid']}, replacement=value,
                                                               upsert=True)


mongo = Mongo(mongodb_pool)
