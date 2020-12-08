import requests as rq
import queue
import random
from time import sleep
#--------------------------------
def init():
    global access_token
    global newMessage
    global server
    global version
    global group_id

    access_token = ''
    version = '5.126'
    group_id = ''
    newMessage = queue.Queue()
    server = {}
#--------------------------------
def lpsInit():
    lps = 'https://api.vk.com/method/groups.getLongPollServer?'
    lps += 'v=' + version
    lps += '&group_id=' + group_id
    lps += '&access_token=' + access_token
    r = rq.get(lps)
    print(r.text)
    server.update(r.json()["response"])
#--------------------------------
def lpsCheck(json):
    text = json["server"]
    text += "?act=a_check&key="
    text += json["key"]
    text += "&ts="
    text += json["ts"]
    text += "&wait=60"
    return text
#--------------------------------
def printMessage(message, user):
    newMsg = []
    maxSize = 1000
    while 1:
        newMsg.append(message[:maxSize])
        if not len(message) > maxSize:
            break
        message = message[maxSize:]
    r = ''
    print(newMsg)
    print(len(newMsg))
    for msg in newMsg:
        text = 'https://api.vk.com/method/messages.send?'
        text += 'v=' + version
        text += '&peer_id=' + str(user)
        text += "&random_id=" + str(random.getrandbits(64))
        text += "&message=" + msg
        text += "&access_token=" + access_token
        r += rq.get(text).text
        if len(newMsg) > 1:
            sleep(2)
    return r
