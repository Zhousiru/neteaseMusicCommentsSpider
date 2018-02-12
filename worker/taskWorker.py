# -*- coding: UTF-8 -*-

import queue
import time
import sys
import logging
from multiprocessing.managers import BaseManager
from getComms import *

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3340.0 Safari/537.36"
}

taskQueue = queue.Queue()
resultQueue = queue.Queue()

logger = logging.getLogger("Task Worker")
formatter = logging.Formatter('%(asctime)s %(levelname)-5s: %(message)s')

fileHandler = logging.FileHandler("worker.log")
fileHandler.setFormatter(formatter)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.formatter = formatter

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

logger.setLevel(logging.DEBUG)


class QueueManager(BaseManager):
    pass


def connectServer(manager):
    while True:
        try:
            manager.connect()
        except ConnectionRefusedError:
            logger.error('Server refused the connection, try to reconnect...')
            time.sleep(5)
            continue

        return 0


def main():
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')

    serverAddr = '127.0.0.1'
    logger.info("Connect to server: %s...", serverAddr)
    manager = QueueManager(address=(serverAddr, 65535),
                           authkey=b'NeteaseMusicSpider')
    while True:
        connectServer(manager)
        logger.info("Getting task queue...")

        task = manager.get_task_queue()
        result = manager.get_result_queue()
        while True:
            try:
                taskInfo = task.get(timeout=5)
                logger.debug("Task: %s", taskInfo)
                result.put(get10Comms(
                    headers, taskInfo['songId'], taskInfo['offset']))
            except ConnectionResetError:
                logger.error('Connection is reset, try to reconnect...')
                break


if __name__ == "__main__":
    main()
    logger.removeHandler(fileHandler)
