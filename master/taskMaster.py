# -*- coding: UTF-8 -*-

import queue
import sys
import time
from multiprocessing.managers import BaseManager
import math
import logging
from getComms import *
from mongoDb import *

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3340.0 Safari/537.36"
}
songIdList = [520461943, 33469232]

taskQueue = queue.Queue()
resultQueue = queue.Queue()

logger = logging.getLogger("Task Master")
formatter = logging.Formatter('%(asctime)s %(levelname)-5s: %(message)s')

fileHandler = logging.FileHandler("master.log")
fileHandler.setFormatter(formatter)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.formatter = formatter

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

logger.setLevel(logging.DEBUG)


class QueueManager(BaseManager):
    pass


def returnTaskQueue():
    return taskQueue


def returnResultQueue():
    return resultQueue


def main():
    QueueManager.register('get_task_queue', callable=returnTaskQueue)
    QueueManager.register('get_result_queue', callable=returnResultQueue)

    manager = QueueManager(address=('127.0.0.1', 65535),
                           authkey=b'NeteaseMusicSpider')
    manager.start()

    task = manager.get_task_queue()
    result = manager.get_result_queue()

    allPollCount = 0
    logger.info("Generate queue...")
    for songId in songIdList:
        pollCount = math.ceil(getCommsCount(headers, songId) / 10)
        allPollCount += pollCount
        for i in range(pollCount):
            offset = i * 10
            task.put({
                'songId': songId,
                'offset': offset
            })
            logger.debug("songId = %d, offset = %d", songId, offset)
    logger.debug("All poll count: %d", allPollCount)

    logger.info("Connect to MongoDB...")
    commColl = mongoConn()

    logger.info("Waiting for result...")
    for i in range(allPollCount):
        commsList = result.get(timeout=20)
        for commDict in commsList:
            procComm(commDict, songId)
            try:
                save(commColl, commDict)
            except pymongo.errors.ServerSelectionTimeoutError:
                logger.error("MongoDB is timeout.")

                return -1

    logger.info("Shutting down queue manager...")
    manager.shutdown()

    return 0


if __name__ == "__main__":
    main()
    logger.removeHandler(fileHandler)
