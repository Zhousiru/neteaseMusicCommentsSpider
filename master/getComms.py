# -*- coding: UTF-8 -*-

import requests
import json
import math
from playload import *

commJsonBaseUrl = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%d"


def getCommsJsonResponse(headers, songId, offset=0):
    playload = getPlayload({
        'username': '',
        'password': '',
        'rememberLogin': 'true',
        'offset': offset
    })

    return requests.post(commJsonBaseUrl % songId, headers=headers, data=playload)


def getCommsCount(headers, songId):
    return json.loads(getCommsJsonResponse(headers, songId).text)['total']


def get10Comms(headers, songId, offset):
    return json.loads(getCommsJsonResponse(headers, songId, offset).text)['comments']
