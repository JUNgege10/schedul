import logging
import redis
import pymongo
import pymysql

class Config(object):
    SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ouyi12345@127.0.0.1:3306/ouyi_project'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:ouyi12345@127.0.0.1:3306/ouyi_project'
    #MONGO_URI = "mongodb://127.0.0.1:27017/?authSource=pyfly&authMechanism=SCRAM-SHA-1"
    MONGO_URI = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    SQLALCHEMY_TRACK_MODUFICATIONS = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_RECYCLE = 800
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
   # REDIS_PASSWD = "jjker1314"
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 86400
    LEVEL = logging.DEBUG

# 开发环境
class DevelopConfig(Config):
    pass
# 生产环境
class ProductConfig(Config):
    DEBUG = False
    LEVEL = logging.ERROR

# 测试环境
class TestingConfig(Config):
    TESTING = True
# 通过统一的字典进行配置类的访问
config_dict = {
    "develop":DevelopConfig,
    "product":ProductConfig,
    "testing":TestingConfig,
}
