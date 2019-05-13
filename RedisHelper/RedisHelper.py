from redis import  StrictRedis, ConnectionPool




class RedisHandler(object):
    """
    完成所有对redis的操作
    """
    def __init__(self, host, port, db, password):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    def connectDataBase(self):
        """
         连接数据库
        """
        try:
            self.pool = ConnectionPool(host=self.host,port=self.port,db=self.db,password=self.password)
            self.redis = StrictRedis(connection_pool=self.pool)
        except:
            return False
        return True

    def sismember(self, key, value):
        '''
        向redis请求是键否存在某元素
        '''
        try:
            if self.redis.sismember(key, value):
                return True
            else:
                return False
        except:
            return False

    def smembers(self, key):
        '''
        从redis集合中取出一个数据
        '''
        try:
            value = self.redis.smembers(key)
        except:
            return None
        return value

    def sadd(self, key, value):
        '''
        向redis集合中添加元素
        '''
        try:
            self.redis.sadd(key, value)
        except:
            return False
        return True

    def smove(self, key1, key2, value):
        '''
        将value从key1移动到key2
        '''
        try:
            self.redis.smove(key1,key2,value)
        except:
            return False
        return True

    def srem(self, key, value):
        try:
            self.redis.srem(key, value)
        except:
            return False
        else:
            return True

    def exists(self, key):
        '''
        向redis请求是否存在键
        '''
        try:
            if self.redis.exists(key):
                return True
            else:
                return False
        except:
            return False

    def spop(self, key):
        '''
        从redis集合中取出一个数据
        '''
        try:
            value = self.redis.spop(key)
        except:
            return None
        return value

    def scard(self, key):
        '''
        从redis集合中取出一个数据
        '''
        try:
            num = self.redis.scard(key)
        except:
            return 0
        return num


    def rpop(self, key):
        '''
        从redis列表右侧取出一个数据
        '''
        try:
            value = self.redis.rpop(key)
        except:
            return None
        return value

    def lpop(self, key):
        '''
        从redis列表左侧取出一个数据
        '''
        try:
            value = self.redis.lpop(key)
        except:
            return None
        return value


    def lpush(self, key, value):
        '''
        从redis列表左侧添加一个数据
        '''
        try:
            value = self.redis.lpush(key, value)
        except:
            return None
        return value

    def rpush(self, key, value):
        '''
        从redis列表左侧添加一个数据
        '''
        try:
            value = self.redis.rpush(key, value)
        except:
            return None
        return value

    # def lrange(self, key, start, end):
    #     '''
    #     从redis列表左侧添加一个数据
    #     '''
    #     try:
    #         value = self.redis.lrange(key, start, end)
    #     except Exception as e:
    #         print(e)
    #         return None
    #     return value


    def delete(self, key):
        '''
        从redis列表删除一个键
        '''
        try:
            self.redis.delete(key)
        except:
            return False
        return True

    def ping(self):
        try:
            self.redis.ping()
        except :
            return False
        else:
            return True

    def zrangebyscore(self, key, MIN_SCORE, MAX_SCORE):
        try:
            values  = self.redis.zrangebyscore(key, MIN_SCORE, MAX_SCORE)
            return values
        except:
            return []

    def zrange(self, key,start=0,end=100,desc=False):
        try:
            values  = self.redis.zrange(key,start=start,end=end,desc=desc)
            return values
        except:
            return []

    def zscore(self, key, value):
        try:
            values  = self.redis.zscore(key, value)
            return values
        except:
            return 99999999999

    def zincrby(self, key, num, value):
        try:
            self.redis.zincrby(key, num, value)
        except:
            return False
        else:
            return True


    def zrem(self, key, value):
        try:
            self.redis.zrem(key, value)
        except:
            return False
        else:
            return True

    def zadd(self, key, value):
        try:
            self.redis.zadd(key, value)
        except:
            return False
        else:
            return True


    def keys(self):
        try:
            value  = self.redis.keys()
        except:
            return None
        else:
            return value


