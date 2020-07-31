import redis
from os import environ





class RedisClient():
    REDIS_HOST = environ.get('REDIS_HOST')
    REDIS_PORT = environ.get('REDIS_PORT')

    def __init__(self):
        self.client = redis.Redis(host=RedisClient.REDIS_HOST, port=RedisClient.REDIS_PORT)

    def saveToRedis(self, key,*values):
        self.client.rpush(key, *values)

    def getFullList(self, key):
        data = self.client.lrange(key, 0, -1)
        return data

    def delete(self, key):
        self.client.delete(key)