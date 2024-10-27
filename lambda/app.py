import os
from decouple import config
import pymongo
import logging
import datetime
import time
import boto3
from json import dumps
from json import loads

ENV = config('ENV')
DB_HOST = config('DB_HOST')
DB_NAME = config('DB_NAME')
DB_PORT = config('DB_PORT', cast=str)
DB_TABLE = config('DB_TABLE')
STATUS_CODE = 200
RESPONSE = {}


def set_logger_level():
    if ENV == 'local':
        return logging.DEBUG
    elif ENV == 'dev':
        return logging.INFO
    else:
        return logging.ERROR


logger = logging.getLogger()
logger_level = set_logger_level()
logger.setLevel(logger_level)


logger.debug("==========")
for key in os.environ:
    logger.debug(f"{key}: {os.environ[key]}")
logger.debug("==========")

try:
    myclient = pymongo.MongoClient(f"mongodb://{DB_HOST}:{DB_PORT}/")
    logger.info("Connected to MongoDB")
except Exception as e:
    logger.error("Could not connect to MongoDB")
    logger.error(e)


def handler(event, context):
    logger.info(event)

    mydb = myclient[DB_NAME]
    mycol = mydb[DB_TABLE]

    x = mycol.insert_one(event)
    logger.debug(str(x.inserted_id))

    mydoc = mycol.find()

    logger.debug(myclient.list_database_names())

    return {
        "isBase64Encoded": False,
        "statusCode": STATUS_CODE,
        "body": dumps(RESPONSE),
        "headers": {
            'content-Type': 'application/json',
            'charset': 'utf8',
            'Access-Control-Allow-Origin': '*'
        }
    }
