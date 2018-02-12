# -*- coding: UTF-8 -*-

import pymongo
import json


def mongoConn(host='127.0.0.1', port=27017, dbName='netease_music'):
    client = pymongo.MongoClient(host, port)
    commColl = client[dbName]['comments']

    return commColl


def procComm(commDict, songId):
    commDict['_id'] = commDict.pop('commentId')
    commDict['songId'] = songId

    return 0


def save(commColl, commDict):
    return commColl.save(commDict)
